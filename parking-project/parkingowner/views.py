from os import close
from urllib import response
from django.shortcuts import render
from numpy import true_divide
import pytz
from rest_framework.views import APIView
from carowner.models import Comment, Reservation
from carowner.serializers import CommentSerializer, ReservationSerializer
from rest_framework.reverse import reverse
import parking
from users.models import CustomUser
from .models import ParkingOwner,Parking, Period, Template,Validation
from .serializers import ParkingOwnerSerializer, ParkingSerializer, PeriodSerializer, TemplateSerializer,ValidationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from django.shortcuts import get_object_or_404,get_list_or_404
from .pagination import ParkingListPagination
from django.utils import timezone
from datetime import date, datetime, timedelta
from dateutil import parser
from django.db.models import F, Q, Count
from rest_framework import viewsets


#########################################################################
#------------------------ Parking related views ------------------------#
#########################################################################

#Create a parking and add it to database
class ParkingCreate(APIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def post(self,request,*args, **kwargs):
		#Create a ParkingOwner model object and filter it by the user whom sent the request.
		owner = get_object_or_404(ParkingOwner, user = request.user)
		#Call serializer
		serializer=ParkingSerializer(data=request.data)

		#Save data if it's valid
		if(serializer.is_valid()):
			serializer.save(owner=owner)
			return Response(serializer.data)

		#Shows error if it's not valid
		else:
			return Response(serializer.errors)

#Edit parking information & delete validation form if it's confirmed or pending.
class ParkingUpdate(generics.RetrieveUpdateAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def update(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		partial = kwargs.pop('partial', True)
		instance = get_object_or_404(Parking, id=request.data['id'],owner=owner)
		instance.isvalid=False

		#if parking name or parking location changes then validation form will be deleted.
		if(request.data.get('parkingName') != None or request.data.get('location') != None):
			if(instance.validationStatus=='V' or instance.validationStatus=='P'):

				Pname=request.data['parkingName']
				Ploc=request.data['location']

				#if there is an extra space or Capital letter in update form, then validation will not expire.
				if(Pname.strip().casefold()!=instance.parkingName.casefold() or 
				Ploc.strip().casefold()!=instance.location.casefold()):
					instance.validationStatus='I'
					instance.save()
					validation=get_object_or_404(Validation,parking=instance).delete()
				
				else:
					pass


		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)


#Edit template of a parking by its id
class EditParkingTemplate(generics.UpdateAPIView):
	queryset = Template.objects.all()
	serializer_class = TemplateSerializer

	def update(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		partial = kwargs.pop('partial', True)
		parking = get_object_or_404(Parking, id=request.data['id'],owner=owner)

		weekDays = []
		for i in request.data.get('days'):
			if i.get('day') is not None and i.get('is_selected'):
				weekDays.append(i.get('day')) 

		#Updating template

		startTime = parser.parse(request.data['openAt'])
		endTime = parser.parse(request.data['closeAt'])

		periods = Period.objects.all().filter(parking=parking,weekDay__in = weekDays)

		templates = Template.objects.all().filter(parking=parking, weekDay__in = weekDays)
		templates.update(openAt = startTime, closeAt = endTime)

		if self.reserveExists(parking,periods):
			return Response({"message" : "dar baze haye entekhabi shoma reserve vojud darad. taghirate shoma az hafte ayande emal khahad shod."},status=status.HTTP_200_OK)
		else:
			for period in periods.order_by('startTime'):

				if templates[0].closeAt.hour == 0:
					closeAt = 24 * 60
				else:
					closeAt = templates[0].closeAt.hour * 60 + templates[0].closeAt.minute

				openAt = templates[0].openAt.hour * 60 + templates[0].openAt.minute
				periodStartTime = period.startTime.hour * 60 + period.startTime.minute

				if period.endTime.hour == 0:
					periodEndTime = 24 * 60
				else:
					periodEndTime = period.endTime.hour * 60 + period.endTime.minute
				

				if periodStartTime >= openAt and periodEndTime <= closeAt:
					period.is_active = True
				else:
					period.is_active = False
				period.save()


		serializer = self.get_serializer(templates, many=True)
		return Response(serializer.data)



	def reserveExists(self,parking,periods):
		orderedperiods = periods.order_by('startTime')
		startPeriod = orderedperiods.first()
		endPeriod = orderedperiods.last()
		reserves = Reservation.objects.all().filter(parking=parking).filter(~Q(Q(endTime__lt = startPeriod.startTime) | Q(startTime__gt=endPeriod.endTime)))
		if reserves.exists():
			return True
		return False

#Get Template of a parking owned by the logged in user by id
class TemplateDetail(generics.ListAPIView):
	queryset = Template.objects.all()
	serializer_class = TemplateSerializer

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, id = request.query_params['parking_id'],owner = owner)
		queryset = Template.objects.filter(parking = parking).order_by('weekDay')

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)



#This view delete a parking by its id(in body)
class ParkingDelete(generics.RetrieveDestroyAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def delete(self, request,*args, **kwargs):
		#Get object by it's id and destroy it.
		owner = get_object_or_404(ParkingOwner, user = request.user)
		instance = get_object_or_404(Parking, id=request.data['id'],owner=owner)
		self.perform_destroy(instance)
		return Response({"message" : "Parking deleted successfully"})


#This view shows registered parking for a parking owner.
class ParkingList(generics.ListAPIView):
	pagination_class=ParkingListPagination
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer
	
	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		queryset = Parking.objects.all().filter(owner = owner)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

#Shows a parking details by its id(in url)
class ParkingDetail(APIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer
	
	def get(self, request,*args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, id = request.GET['id'], owner = owner)
		serializer = ParkingSerializer(parking)
		return Response(serializer.data)

#########################################################################
#--------------------- ParkingOwner related views ----------------------#
#########################################################################

#Shows list of registered parkings
class ParkingOwnerList(generics.ListAPIView):
	queryset = ParkingOwner.objects.all()
	serializer_class = ParkingOwnerSerializer

#Shows parking owner details by its id(in url)
class ParkingOwnerDetail(generics.RetrieveAPIView):
	queryset = ParkingOwner.objects.all()
	serializer_class = ParkingOwnerSerializer

#Edit parking owners profile
class ParkingOwnerUpdate(generics.RetrieveUpdateAPIView):
	queryset = ParkingOwner.objects.all()
	serializer_class = ParkingOwnerSerializer

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', True)
		instance = get_object_or_404(ParkingOwner, user = request.user)
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)

#########################################################################
#--------------------- Validations related views -----------------------#
#########################################################################

#This view validate a parking information.
class Validator(generics.CreateAPIView):
	queryset=Validation.objects.all()
	serializer_class=ValidationSerializer

	def _get_queryset(klass):
		if hasattr(klass, '_default_manager'):
			return klass._default_manager.all()
		return klass

	def get_object_or_404(klass, *args, **kwargs):
		queryset = Validator._get_queryset(klass)
		if not hasattr(queryset, 'get'):
			klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
			raise ValueError(
				"First argument to get_object_or_404() must be a Model, Manager, "
				"or QuerySet, not '%s'." % klass__name
			)
		try:
			return queryset.get(*args, **kwargs)
		except queryset.model.DoesNotExist:
			return "Does not exist"

	def post(self,request,*args, **kwargs):		
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking,id=request.data['id'],owner=owner)
		
		#Call serializer
		serializer=ValidationSerializer(data=request.data)

		#Save data if it's valid
		if(serializer.is_valid()):
			serializer.save(parking=parking)
			parking.validationStatus="P"
			parking.save()
			return Response(serializer.data)

		#Shows error if it's not valid
		else:
			return Response(serializer.errors)

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, id = request.GET['id'], owner = owner)
		# validation=get_object_or_404(Validation,parking=parking)
		# time=datetime.now(timezone.utc)-validation.time_Added
		# serializer = self.get_serializer(validation)
		nationalCode_blacklist=['0440833242','0228763243','01223454512','0333453823']
		# print(time.total_seconds())

		if(Validator.get_object_or_404(Validation,parking=parking)!="Does not exist"):
			
			validation=get_object_or_404(Validation,parking=parking)
			serializer = ValidationSerializer(validation)
			time=datetime.now()-validation.time_Added
			print(time.total_seconds())

			if(time.total_seconds()>30):

				if(validation.nationalCode in nationalCode_blacklist):
					parking.validationStatus="I"
					parking.save()
					validation=get_object_or_404(Validation,parking=parking).delete()
					return Response(serializer.data)
				else:
					parking.validationStatus="V"
					parking.save()
					return Response(serializer.data)

			else:
				return Response(serializer.data)
		
		else:
			serializer2=ParkingSerializer(parking)
			return Response(serializer2.data)

#shows and updates period list of a parking
#it should be called every 30 minutes !
class PeriodsList(generics.ListAPIView):
	queryset = Period.objects.all()
	serializer_class = PeriodSerializer

	def get(self, request, *args, **kwargs):
		parking = get_object_or_404(Parking, id=request.GET['parkingId'])
		periods = Period.objects.all().filter(parking=parking)

		currentPeriod = PeriodsList.get_current_period(parking)

		passedPeriods = periods.filter(endTime__lte=currentPeriod.startTime)

		for period in passedPeriods:
			template = get_object_or_404(Template, parking=parking, weekDay=period.weekDay)
			openAt = template.openAt.hour * 60 + template.openAt.minute
			closeAt = template.closeAt.hour * 60 + template.closeAt.minute
			periodStartTime = period.startTime.hour * 60 + period.startTime.minute
			periodEndTime = period.endTime.hour * 60 + period.endTime.minute

			if periodStartTime >= openAt or periodEndTime <= closeAt:
				period.is_active = True
			else:
				period.is_active = False
			period.save()

		passedPeriods.update(capacity=parking.capacity, startTime=F('startTime') + timedelta(days=7),
							 endTime=F('endTime') + timedelta(days=7))

		queryset = periods.filter(is_active=True, startTime__gte=currentPeriod.startTime).order_by('startTime')[:48]

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	@staticmethod
	def get_current_period(parking):
		today = datetime.today().weekday()
		now = datetime.now()

		if now.minute >= 30:
			currentPeriod = get_object_or_404(Period, parking=parking, startTime__hour=now.hour, startTime__minute=30,
											  weekDay=today)
		else:
			currentPeriod = get_object_or_404(Period, parking=parking, startTime__hour=now.hour, startTime__minute=0,
											  weekDay=today)

		return currentPeriod

	@staticmethod
	def get_current_period_ids_if_has_capacity():
		today = datetime.today().weekday()
		now = datetime.now()

		if now.minute >= 30:
			current_periods = list(Period.objects.filter(
				startTime__hour=now.hour, startTime__minute=30, weekDay=today, capacity__gt=0).values_list('id',
																										   flat=True))
		else:
			current_periods = list(Period.objects.filter(
				startTime__hour=now.hour, startTime__minute=0, weekDay=today, capacity__gt=0).values_list('id',
																										  flat=True))

		return current_periods

	@staticmethod
	def update_all_periods():
		parkings = Parking.objects.all()
		for parking in parkings:
			periods = Period.objects.all().filter(parking=parking)

			currentPeriod = PeriodsList.get_current_period(parking)

			passedPeriods = periods.filter(endTime__lte=currentPeriod.startTime)

			for period in passedPeriods:
				template = get_object_or_404(Template, parking=parking, weekDay=period.weekDay)
				openAt = template.openAt.hour * 60 + template.openAt.minute
				closeAt = template.closeAt.hour * 60 + template.closeAt.minute
				periodStartTime = period.startTime.hour * 60 + period.startTime.minute
				periodEndTime = period.endTime.hour * 60 + period.endTime.minute

				if periodStartTime >= openAt or periodEndTime <= closeAt:
					period.is_active = True
				else:
					period.is_active = False
				period.save()

			passedPeriods.update(capacity=parking.capacity, startTime=F('startTime') + timedelta(days=7),
								 endTime=F('endTime') + timedelta(days=7))


#Gets the current period of a parking
class CurrentPeriod(generics.RetrieveAPIView):
	queryset = Period.objects.all()
	serializer_class = PeriodSerializer

	def get(self, request, *args, **kwargs):
		parking = get_object_or_404(Parking, id = request.GET['parkingId'])
		today = datetime.today().weekday()
		now = datetime.now()

		if now.minute >= 30:
			currentPeriod = get_object_or_404(Period, parking = parking,startTime__hour = now.hour, startTime__minute = 30,weekDay=today)
		else:
			currentPeriod = get_object_or_404(Period, parking = parking,startTime__hour = now.hour, startTime__minute = 0,weekDay=today)

		serializer = self.get_serializer(currentPeriod)
		return Response(serializer.data)


#changes the capacity of a parking manually with status in body
class ManualEnterOrExit(generics.UpdateAPIView):
	queryset = Period.objects.all()
	serializer_class = PeriodSerializer

	def put(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, owner = owner,id = request.data['parkingId'])
		today = datetime.today().weekday()

		now = datetime.now()
		if now.minute >= 30:
			currentPeriod = get_object_or_404(Period, parking = parking,is_active=True,startTime__hour = now.hour, startTime__minute = 30,weekDay=today)
		else:
			currentPeriod = get_object_or_404(Period, parking = parking,is_active=True,startTime__hour = now.hour, startTime__minute = 0,weekDay=today)

		periods = Period.objects.all().filter(parking = parking)
		if request.data['status'] == 'enter':
			if currentPeriod.capacity == 0:
				return Response({'message' : 'Capacity cant be below 0'})
			periods.update(capacity = F('capacity') - 1)
		elif request.data['status'] == 'exit':
			if currentPeriod.capacity >= parking.capacity:
				return Response({'message' : 'capacity cant be greater than total capacity'})
			periods.update(capacity = F('capacity') + 1)
		
		currentPeriod.refresh_from_db()

		
		partial = kwargs.pop('partial', True)
		serializer = self.get_serializer(currentPeriod, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)

		if getattr(currentPeriod, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			currentPeriod._prefetched_objects_cache = {}

		return Response(serializer.data)


#returns the list of reservations of a parking for the logged in ParkingOwner
class ReservationListParking(generics.ListAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, owner = owner, id = request.GET['parkingId'])
		now = datetime.now()
		now = now + timedelta(hours=-1)
		queryset = Reservation.objects.all().filter(parking = parking,startTime__gte = now)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


#returns the list of passed reservations of a parking for the logged in ParkingOwner
class PassedReservationListParking(generics.ListAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, owner = owner, id = request.GET['parkingId'])
		now = datetime.now()
		queryset = Reservation.objects.all().filter(parking = parking,endTime__lte = now)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


class CombinedReservesAndComments(generics.ListAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request, *args, **kwargs):
		reserve_queryset = Reservation.objects.all()
		reserve_serializer = ReservationSerializer(reserve_queryset, many = True)

		comment_queryset = Comment.objects.all()
		comment_serializer = CommentSerializer(comment_queryset,many=True)

		# page = self.paginate_queryset(queryset)
		# if page is not None:
		# 	serializer = self.get_serializer(page, many=True)
		# 	return self.get_paginated_response(serializer.data)
		return Response(reserve_serializer.data + comment_serializer.data, status=status.HTTP_200_OK)

#Overall income
class OverallIncome(generics.RetrieveAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request,*args, **kwargs):
		parking = get_object_or_404(Parking, id = request.GET['parkingId'])
		dic={}
		costs=list()
		values=list()
		today=str(datetime.now().date())
		last_week =str(datetime.now().date() - timedelta(days=7))

		interval=request.GET['interval']

		if(interval=="day"):
			queryset = Reservation.objects.all().filter(parking=parking,startTime__gt=today+"T00:00:00",endTime__lt=today+"T23:59:00").order_by('startTime')

		elif(interval=="week"):
			queryset = Reservation.objects.all().filter(parking=parking,startTime__gt=last_week+"T00:00:00",endTime__lt=today+"T23:59:00").order_by('startTime')

		elif(interval=="month"):
			queryset = Reservation.objects.all().filter(parking=parking,startTime__gt=str(datetime.now().date().replace(day=1))+"T00:00:00",endTime__lt=str(datetime.now().date().replace(day=30))+"T23:59:00").order_by('startTime')

		elif(interval=="year"):
			queryset = Reservation.objects.all().filter(parking=parking,startTime__gt=str(datetime.now().date().replace(day=1,month=1))+"T00:00:00",endTime__lt=str(datetime.now().date().replace(day=31,month=12))+"T23:59:00").order_by('startTime')
			
		else:
			return Response({"message" : "Invalid interval"})

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)

		if(len(serializer.data)==0):
			return Response("0")

		elif(interval=="year"):
			for i in range(len(serializer.data)):
				values.append(serializer.data[i]["startTime"][:7])
				costs.append(serializer.data[i]["cost"])

			print(values) 
			print(costs)
			cn=0
			for item in values:
				if (item in dic):
					dic[item] += costs[cn]
				else:
					dic[item] = costs[cn]
				cn+=1
 
			return Response(dic) 
		
		else:  
			for i in range(len(serializer.data)):
				values.append(serializer.data[i]["startTime"][:10])
				costs.append(serializer.data[i]["cost"])

			cn=0
			for item in values:
				if (item in dic):
					dic[item] += costs[cn]
				else:
					dic[item] = costs[cn]
				cn+=1

			return Response(dic)
		
		 
class OverallCustomers(generics.RetrieveAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request,*args, **kwargs):
		parking = get_object_or_404(Parking, id = request.GET['parkingId'])
		values=list()
		dic={}
		today=str(datetime.now().date())
		last_week =str(datetime.now().date() - timedelta(days=7))

		interval=request.GET['interval']

		if(interval=="day"):
			queryset = Reservation.objects.all().filter(parking=parking,startTime__gt=today+"T00:00:00",endTime__lt=today+"T23:59:00").order_by('startTime')

		elif(interval=="week"):
			queryset = Reservation.objects.all().filter(parking=parking,startTime__gt=last_week+"T00:00:00",endTime__lt=today+"T23:59:00").order_by('startTime')

		elif(interval=="month"):
			queryset = Reservation.objects.all().filter(parking=parking,startTime__gt=str(datetime.now().date().replace(day=1))+"T00:00:00",endTime__lt=str(datetime.now().date().replace(day=30))+"T23:59:00").order_by('startTime')

		elif(interval=="year"):
			queryset = Reservation.objects.all().filter(parking=parking,startTime__gt=str(datetime.now().date().replace(day=1,month=1))+"T00:00:00",endTime__lt=str(datetime.now().date().replace(day=31,month=12))+"T23:59:00").order_by('startTime')
			
		else:
			return Response({"message" : "Invalid interval"})

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		
		serializer = self.get_serializer(queryset, many=True)

		if(len(serializer.data)==0):
			return Response("No Customer found in this interval")

		elif(interval=="year"):
			for i in range(len(serializer.data)):
				values.append(serializer.data[i]["startTime"][:7])

			for item in values:
				if (item in dic):
					dic[item] += 1
				else:
					dic[item] = 1
 
			return Response(dic) 
		
		else:  
			for i in range(len(serializer.data)):
				values.append(serializer.data[i]["startTime"][:10])

			for item in values:
				if (item in dic):
					dic[item] += 1
				else:
					dic[item] = 1
	
			return Response(dic)