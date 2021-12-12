from django.shortcuts import render
import pytz
from rest_framework.views import APIView
from carowner.models import Reservation
from carowner.serializers import ReservationSerializer

import parking
from users.models import CustomUser
from .models import ParkingOwner,Parking, Period,Validation
from .serializers import ParkingOwnerSerializer, ParkingSerializer, PeriodSerializer,ValidationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from django.shortcuts import get_object_or_404,get_list_or_404
from .pagination import ParkingListPagination
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.db.models import F, Q
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
				if(Pname.strip().casefold()==instance.parkingName.casefold() or 
				Ploc.strip().casefold()==instance.location.casefold()):
					pass
				
				else:
					instance.validationStatus='I'
					instance.save()
					validation=get_object_or_404(Validation,parking=instance).delete()

		if request.data.get('openAt') != None:
			#Updating template
			weekDay = request.data['date']
			startTime = datetime.strptime(request.data['openAt'],"%H:%M:%S")
			endTime = datetime.strptime(request.data['closeAt'],"%H:%M:%S")
			if startTime.minute >= 30:
				startPeriod = get_object_or_404(Period, parking = instance,startTime__hour = startTime.hour, startTime__minute = 30,weekDay = weekDay)
			else:
				startPeriod = get_object_or_404(Period, parking = instance,startTime__hour = startTime.hour, startTime__minute = 0,weekDay = weekDay)

			endPeriod = get_object_or_404(Period, parking = instance,endTime__hour = endTime.hour, endTime__minute = endTime.minute,weekDay = weekDay)

			startPeriod.is_active = True
			startPeriod.save()
			periods = Period.objects.all().filter(parking=instance,weekDay=weekDay)
			for period in periods:
				if period.startTime.hour >= startPeriod.endTime.hour and period.startTime.hour <= endPeriod.startTime.hour:
					if period.startTime.hour == endPeriod.startTime.hour:
						if period.startTime.minute > endPeriod.startTime.minute:
							period.is_active = False
							period.save()
						else:
							period.is_active = True
							period.save()
					else:
						period.is_active = True
						period.save()
				else:
					if not period == startPeriod:
						period.is_active = False
						period.save()


		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)

#This view delete a parking by its id(in body)
class ParkingDelete(generics.RetrieveDestroyAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def delete(self, request,format=None):
		#Get object by it's id and destroy it.
		owner = get_object_or_404(ParkingOwner, user = request.user)
		instance = get_object_or_404(Parking, id=request.data['id'],owner=owner).delete()
		
		return Response({"message" : "Parking deleted successfully"},status=status.HTTP_204_NO_CONTENT)



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
			time=datetime.now(timezone.utc)-validation.time_Added
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
		parking = get_object_or_404(Parking, id = request.GET['parkingId'])
		today = datetime.today().weekday()
		periods = Period.objects.all().filter(parking = parking)

		now = datetime.now()

		if now.minute >= 30:
			currentPeriod = get_object_or_404(Period, parking = parking,startTime__hour = now.hour, startTime__minute = 30,weekDay=today)
		else:
			currentPeriod = get_object_or_404(Period, parking = parking,startTime__hour = now.hour, startTime__minute = 0,weekDay=today)
		
		passedPeriods = periods.filter(endTime__lte = currentPeriod.startTime)
		passedPeriods.update(capacity = currentPeriod.capacity,startTime = F('startTime') + timedelta(days=7),endTime = F('endTime') + timedelta(days=7))

		queryset = periods.filter(is_active = True, startTime__gte = currentPeriod.startTime).order_by('startTime')[:48]

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)



#changes the capacity of a parking manually with status in body
class ManualEnterOrExit(generics.UpdateAPIView):
	queryset = Period.objects.all()
	serializer_class = PeriodSerializer

	def put(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, owner = owner,id = request.data['parkingId'])
		today = datetime.today().weekday()

		periods = Period.objects.all().filter(parking = parking)
		if request.data['status'] == 'enter':
			periods.update(capacity = F('capacity') - 1)
		elif request.data['status'] == 'exit':
			periods.update(capacity = F('capacity') + 1)

		now = datetime.now()
		if now.minute >= 30:
			currentPeriod = get_object_or_404(Period, parking = parking,is_active=True,startTime__hour = now.hour, startTime__minute = 30,weekDay=today)
		else:
			currentPeriod = get_object_or_404(Period, parking = parking,is_active=True,startTime__hour = now.hour, startTime__minute = 0,weekDay=today)
		
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
		now = now.replace(hour=now.hour-1)
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