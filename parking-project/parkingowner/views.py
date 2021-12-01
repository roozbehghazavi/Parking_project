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
from datetime import date, datetime
from django.db.models import F
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
		template = [[1 for i in range(48)] for j in range(7)]
		#Call serializer
		serializer=ParkingSerializer(data=request.data)

		#Save data if it's valid
		if(serializer.is_valid()):
			serializer.save(owner=owner,template = template)
			return Response(serializer.data)

		#Shows error if it's not valid
		else:
			return Response(serializer.errors)

#Edit parking information
class ParkingUpdate(generics.RetrieveUpdateAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def update(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		partial = kwargs.pop('partial', False)
		instance = get_object_or_404(Parking, id=request.data['id'],owner=owner)
		instance.isvalid=False

		if request.data.get('openAt') != None:
			#Updating template
			startTime = datetime.strptime(request.data['openAt'],"%Y/%m/%d %H:%M:%S")
			endTime = datetime.strptime(request.data['closeAt'],"%Y/%m/%d %H:%M:%S")
			if startTime.minute >= 30:
				startPeriod = get_object_or_404(Period, parking = instance,startTime__hour = startTime.hour, startTime__minute = 30)
			else:
				startPeriod = get_object_or_404(Period, parking = instance,startTime__hour = startTime.hour, startTime__minute = 0)

			endPeriod = get_object_or_404(Period, parking = instance,endTime__hour = endTime.hour, endTime__minute = endTime.minute)
			for i in range(len(instance.template[request.data['date']])):
				if i < startPeriod.index-1 or i > endPeriod.index-1:
					instance.template[request.data['date']][i] = 0
				else:
					instance.template[request.data['date']][i] = 1



		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)

	def perform_update(self, serializer):
		serializer.save()

	def partial_update(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return self.update(request, *args, **kwargs)

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
	
	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		instance = get_object_or_404(Parking, id = request.data['id'], owner = owner)
		serializer = ParkingSerializer(instance)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		instance = get_object_or_404(Parking, id = request.data['id'], owner = owner)
		serializer = ParkingSerializer(instance)
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
		partial = kwargs.pop('partial', False)
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

	def post(self,request,*args, **kwargs):		
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking,id=request.data['id'],owner=owner)
		nationalCode_blacklist=['985']
		#Call serializer
		serializer=ValidationSerializer(data=request.data)

		
		if(request.data['nationalCode'] in nationalCode_blacklist):
			return Response({"message" : "This national code is restricted"})

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
		parking = get_object_or_404(Parking, id = request.data['id'], owner = owner)
		validation=get_object_or_404(Validation,parking=parking)
		time=datetime.now(timezone.utc)-validation.time_Added
		serializer = self.get_serializer(validation)

		if(time.total_seconds()>30): 
			parking.validationStatus="V"
			parking.save()
			return Response(serializer.data)

		else:
			return Response(serializer.data)

class ValidatorGet(generics.CreateAPIView):
	queryset=Validation.objects.all()
	serializer_class=ValidationSerializer
	
	def post(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, id = request.data['id'], owner = owner)
		validation=get_object_or_404(Validation,parking=parking)
		time=datetime.now(timezone.utc)-validation.time_Added
		serializer = self.get_serializer(validation)

		if(time.total_seconds()>30): 
			parking.validationStatus="V"
			parking.save()
			return Response(serializer.data)

		else:
			return Response(serializer.data)

class PeriodsList(generics.ListAPIView):
	queryset = Period.objects.all()
	serializer_class = PeriodSerializer

	def get(self, request, *args, **kwargs):
		parking = get_object_or_404(Parking, id = request.data['parkingId'])
		today = datetime.today().weekday()
		periods = Period.objects.all().filter(parking = parking).order_by('index')
		
		if today == 5 : #Shanbe
			self.setPeriodsOfWeekDay(parking,parking.template[0],periods)
		elif today == 6 : #1shanbe
			self.setPeriodsOfWeekDay(parking,parking.template[1],periods)
		elif today == 0 : #2shanbe
			self.setPeriodsOfWeekDay(parking,parking.template[2],periods)
		elif today == 1 : #3shanbe
			self.setPeriodsOfWeekDay(parking,parking.template[3],periods)
		elif today == 2 : #4shanbe
			self.setPeriodsOfWeekDay(parking,parking.template[4],periods)
		elif today == 3 : #5shanbe
			self.setPeriodsOfWeekDay(parking,parking.template[5],periods)
		else: #jome
			self.setPeriodsOfWeekDay(parking,parking.template[6],periods)

		queryset = periods.filter(is_active = True)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def setPeriodsOfWeekDay(self,parking,template,periods):
		for i in range(len(template)):
			period = periods.get(index = i+1)
			if template[i] == 0:
				period.is_active = False
			else:
				period.is_active = True
			period.save()
		now = datetime.now()
		if now.minute >= 30:
			currentPeriod = get_object_or_404(Period, parking = parking,startTime__hour = now.hour, startTime__minute = 30)
		else:
			currentPeriod = get_object_or_404(Period, parking = parking,startTime__hour = now.hour, startTime__minute = 0)
		
		passedPeriods = periods.filter(index__lt = currentPeriod.index)
		passedPeriods.update(capacity = currentPeriod.capacity)


class ManualEnterOrExit(generics.UpdateAPIView):
	queryset = Period.objects.all()
	serializer_class = PeriodSerializer

	def put(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, owner = owner,id = request.data['parkingId'])
		now = datetime.now()
		if now.minute >= 30:
			currentPeriod = get_object_or_404(Period, parking = parking,is_active=True,startTime__hour = now.hour, startTime__minute = 30)
		else:
			currentPeriod = get_object_or_404(Period, parking = parking,is_active=True,startTime__hour = now.hour, startTime__minute = 0)
		nextPeriods = Period.objects.all().filter(index__gte = currentPeriod.index,parking = parking).order_by('index')
		if request.data['status'] == 'enter':
			nextPeriods.update(capacity = F('capacity') - 1)
		elif request.data['status'] == 'exit':
			nextPeriods.update(capacity = F('capacity') + 1)
		
		partial = kwargs.pop('partial', False)
		serializer = PeriodSerializer(nextPeriods,many = True)

		if getattr(nextPeriods, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			nextPeriods._prefetched_objects_cache = {}

		return Response(serializer.data)


#returns the list of reservations of a parking for the logged in ParkingOwner
class ReservationListParking(generics.ListAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking, owner = owner, id = request.GET['parkingId'])
		queryset = Reservation.objects.all().filter(parking = parking)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)