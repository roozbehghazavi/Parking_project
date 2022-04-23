from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import pytz
from rest_framework.response import Response
import parking
from parkingowner.models import Parking, ParkingOwner, Period
from parkingowner.serializers import ParkingSerializer, PeriodSerializer
from parkingowner.views import PeriodsList
from .models import Car, CarOwner, Comment, Rate, Reservation, ParkingMonitor
from users.models import CustomUser
from .pagination import CarOwnerPagination
from rest_framework import generics, pagination, serializers, status
from .serializers import CarOwnerSerializer, CarSerializer, CommentChildSerializer, CommentSerializer, ReservationSerializer
from django.db.models import Avg, F, Q, Max, Min, Count
import json
import requests
from datetime import date, datetime, timedelta
from rest_framework.views import APIView
from rest_framework import filters
from django.db import transaction
# Create your views here.




### Car Owner Views



class CarOwnerCreate(generics.CreateAPIView):
	# API endpoint that allows creation of a new customer
	queryset = CarOwner.objects.all()
	serializer_class = CarOwnerSerializer

class CarOwnerList(generics.ListAPIView):
	# API endpoint that allows customer to be viewed.
	queryset = CarOwner.objects.all()
	serializer_class = CarOwnerSerializer

#Ruturns logged in CarOwner detail
class CarOwnerDetail(generics.RetrieveAPIView):
	# API endpoint that returns a single customer by pk.
	queryset = CarOwner.objects.all()
	serializer_class = CarOwnerSerializer

	def get(self, request, *args, **kwargs):
		instance = get_object_or_404(CarOwner, user = request.user)
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

#Update logged in CarOwner
class CarOwnerUpdate(generics.RetrieveUpdateAPIView):
	# API endpoint that allows a customer record to be updated.
	queryset = CarOwner.objects.all()
	serializer_class = CarOwnerSerializer

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = get_object_or_404(CarOwner, user = request.user)
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)
	

#Delete logged in CarOwner
class CarOwnerDelete(generics.RetrieveDestroyAPIView):
	# API endpoint that allows a customer record to be deleted.
	queryset = CarOwner.objects.all()
	serializer_class = CarOwnerSerializer

	def delete(self, request, *args, **kwargs):
		get_object_or_404(CarOwner, user = request.user).delete()
		user = self.request.user
		user.delete()

		return Response({"message" : "CarOwner deleted successfully"},status=status.HTTP_204_NO_CONTENT)




### Car Views 



#Creates a car for the logged in CarOwner
class CarCreate(generics.CreateAPIView):
	# API endpoint that allows creation of a new customer
	queryset = Car.objects.all()
	serializer_class = CarSerializer

	def create(self, request, *args, **kwargs):
		owner = get_object_or_404(CarOwner, user = request.user)
		serializer = CarSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(owner=owner)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



#Shows List of all Cars Owned by the Logged in user
class CarList(generics.ListAPIView):
	# API endpoint that allows customer to be viewed.
	queryset = Car.objects.all()
	serializer_class = CarSerializer
	pagination_class = CarOwnerPagination

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(CarOwner, user = request.user)
		queryset = Car.objects.all().filter(owner = owner).order_by('carName')

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

#Returns Detail of a Car by id owned by the logged in CarOwner
class CarDetail(generics.RetrieveAPIView):
	# API endpoint that returns a single customer by pk.
	queryset = Car.objects.all()
	serializer_class = CarSerializer

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(CarOwner, user = request.user)
		instance = get_object_or_404(Car, id = request.GET['id'], owner = owner)
		serializer = self.get_serializer(instance)
		return Response(serializer.data)


#Update a Car by id owned by the logged in CarOwner
class CarUpdate(generics.RetrieveUpdateAPIView):
	# API endpoint that allows a customer record to be updated.
	queryset = Car.objects.all()
	serializer_class = CarSerializer

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', True)
		owner = get_object_or_404(CarOwner, user = request.user)
		instance = get_object_or_404(Car, id = request.data['id'], owner = owner)
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)

#Delete a Car by id owned by the logged in CarOwner
class CarDelete(generics.RetrieveDestroyAPIView):
	# API endpoint that allows a customer record to be deleted.
	queryset = Car.objects.all()
	serializer_class = CarSerializer

	def delete(self, request, *args, **kwargs):
		owner = get_object_or_404(CarOwner, user = request.user)
		instance = get_object_or_404(Car, id = request.data['id'], owner = owner)
		self.perform_destroy(instance)
		return Response({"message" : "Car deleted successfully"},status=status.HTTP_204_NO_CONTENT)




# Parking views for CarOwner



#Shows List of all parkings ordering by parking name for CarOwner
class ParkingList(generics.ListAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer
	pagination_class = CarOwnerPagination

	def get(self, request, *args, **kwargs):
		PeriodsList.update_all_periods()
		queryset = Parking.objects.all().filter(validationStatus = "V").order_by('parkingName')

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)




#Comment views for CarOwner



#Create a comment for a parking with id in body owned by the logged in Car Owner
class CommentParentCreate(generics.CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def create(self, request, *args, **kwargs):
		author = get_object_or_404(CustomUser, email = request.user.email)
		parking = get_object_or_404(Parking, id = request.data['parkingId'])
		serializer = CommentSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(author=author, parking = parking)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


#Edit a comment by its id owned by the logged in user
class CommentUpdate(generics.RetrieveUpdateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def put(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		author = get_object_or_404(CustomUser, email = request.user.email)
		instance = get_object_or_404(Comment, id = request.data['id'], author = author)
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)



#Delete a comment by its id owned by the logged in user
class CommentDelete(generics.DestroyAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def delete(self, request, *args, **kwargs):
		author = get_object_or_404(CustomUser, email = request.user.email)
		instance = get_object_or_404(Comment, id = request.data['id'], author = author)
		self.perform_destroy(instance)
		return Response({"message" : "Comment deleted successfully"},status=status.HTTP_204_NO_CONTENT)



#Add a reply to a comment by passing parking id and parent id
class CommentChildCreate(generics.CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentChildSerializer

	def create(self, request, *args, **kwargs):
		author = get_object_or_404(CustomUser, email = request.user.email)
		parent = get_object_or_404(Comment, id = request.data['parentId'])
		parking = get_object_or_404(Parking, id = parent.parking.id)
		serializer = CommentChildSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(author=author, parking = parking, parent = parent)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


#Shows list of comments for a parking with id
class CommentList(generics.ListCreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def get(self, request,*args, **kwargs):
		parking = get_object_or_404(Parking, id = request.GET['id'])
		queryset = Comment.objects.all().filter(parking = parking).order_by('-dateAdded')

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)



### Rating methods


#Add a rating for a parking by id
class AddRate(generics.UpdateAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def put(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		value = request.data['value']
		if value > 5 :
			return Response({"message" : "value must be less than or equal to 5"}, status=status.HTTP_400_BAD_REQUEST)
		instance = get_object_or_404(Parking, id = request.data['id'])
		owner = get_object_or_404(CarOwner, user = request.user)
		newRate = Rate.objects.all().filter(parking = instance, owner = owner).first()
		if newRate == None :
			newRate = Rate.objects.create(parking = instance , owner = owner, value = value)
			newRate.save()
		else:
			newRate.delete()
			newRate = Rate.objects.create(parking = instance , owner = owner, value = value)
			newRate.save()
		rating = Rate.objects.all().filter(parking = instance).aggregate(Avg('value'))['value__avg']
		instance.rating = round(rating,1)

		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)


#Shows whether the user rated a parking or not
class IsRated(generics.RetrieveAPIView):
	queryset = Rate.objects.all()

	def get(self, request, *args, **kwargs):
		parking = get_object_or_404(Parking, id = request.GET['id'])
		owner = get_object_or_404(CarOwner, user = request.user)
		instance = Rate.objects.all().filter(parking = parking, owner = owner).first()

		if instance != None :
			return Response({'isRated':instance.value},status=status.HTTP_200_OK)
		elif instance == None :
			return Response({'isRated':False},status=status.HTTP_200_OK)

		return Response({'message':'error'},status=status.HTTP_400_BAD_REQUEST)



#reserves a parking with startTime and endTime 
#returns a reservation if the parking has capacity available , otherwise it returns the list of periods that are filled
class ReservationCreate(generics.CreateAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		instance = get_object_or_404(CustomUser, id = request.user.id)
		owner = get_object_or_404(CarOwner, user = request.user)
		parking = get_object_or_404(Parking, id = request.data['parking_id'])
		car = get_object_or_404(Car,id = request.data['car_id'],owner = owner)
		startTime = datetime.strptime(request.data['enter'],"%Y/%m/%d %H:%M:%S")
		endTime = datetime.strptime(request.data['exit'],"%Y/%m/%d %H:%M:%S")
		periods = self.getPeriods(startTime,endTime,parking)
		isValid = self.checkValidation(periods)
		pay_with_credit = request.data.get('pay_with_credit', False)

		#returns true if the user has a reservation on this period
		isReserved = Reservation.objects.filter(~Q(Q(endTime__lte = startTime) | Q(startTime__gte = endTime))).filter(car=car).exists()
		if isReserved:
			return Response({'message' : 'You have a reservation on this period'}, status=status.HTTP_400_BAD_REQUEST)

		if isValid == True: #creates the reservation if True
			periods.update(capacity = F('capacity') - 1)
			serializer = ReservationSerializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			duration = ((endTime - startTime).total_seconds())/60
			pricePerMin = parking.pricePerHour/60
			cost = round(duration * pricePerMin,1)
			if pay_with_credit:
				owner.credit = F('credit') - cost
				owner.save()
			trackingCode = 0
			if Reservation.objects.filter(parking=parking).count() > 0:
				trackingCode = Reservation.objects.filter(parking=parking).count()
			serializer.save(owner = owner,parking=parking,startTime=startTime,endTime=endTime,cost = cost,car = car,trackingCode=trackingCode)
			headers = self.get_success_headers(serializer.data)
			text="رزرو شما با موفقیت انجام شد" + "\n" +"کد رهگیری شما" +"\n" + str(trackingCode)
			data = {'from': '50004001885294', 'to': instance.phoneNumber , 'text': text}
			response = requests.post('https://console.melipayamak.com/api/send/simple/7557787143184d838512628417a5001f', json=data)
			return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

		elif isValid == "Error, Closed Periods Found !": #returns the list of closed periods
			return Response({'message' : isValid})

		else: #returns the list of filled periods
			queryset = isValid
			serializer = PeriodSerializer(queryset,many = True)
			return Response(serializer.data)

	#returns the list of periods with a startTime and endTime
	def getPeriods(self,startTime,endTime,parking):
		
		if startTime.minute >= 30:
			startPeriod = get_object_or_404(Period, parking = parking,startTime__day = startTime.day,startTime__hour = startTime.hour, startTime__minute = 30)
		else:
			startPeriod = get_object_or_404(Period, parking = parking,startTime__day = startTime.day,startTime__hour = startTime.hour, startTime__minute = 0)

		periods = Period.objects.all().filter(parking = parking, startTime__gte = startPeriod.startTime, endTime__lte = endTime)
		return periods
		
	#check if the periods are available
	def checkValidation(self,periods):
		filledPeriods = periods.filter(capacity = 0)
		notActivePeriods = periods.filter(is_active = False)
		if notActivePeriods.count() != 0:
			return "Error, Closed Periods Found !"
		elif filledPeriods.count() == 0 :
			return True
		else:
			return filledPeriods

#Delete a reservation
class ReservationDelete(generics.DestroyAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def destroy(self, request, *args, **kwargs):
		usr = get_object_or_404(CustomUser, id = request.user.id)
		instance = get_object_or_404(Reservation, id=request.data.get('id'))
		if instance.startTime - timedelta(minutes=30) < datetime.now():
			return Response({'message': 'امکان لغو رزرو در این بازه زمانی وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)
		else:
			self.perform_destroy(instance)
			instance.owner.credit = F('credit') + instance.cost
			text = 'رزرو شما با موفقیت لغو شد و هزینه آن به کیف پول شما برگشت داده شد'
			data = {'from': '50004001885294', 'to': usr.phoneNumber , 'text': text}
			return Response({'message': 'رزرو شما با موفقیت لغو شد و هزینه آن به کیف پول شما برگشت داده شد'}, status=status.HTTP_204_NO_CONTENT)

#returns the list of reservations for the logged in carowner from now on
class ReservationListCarOwner(generics.ListAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(CarOwner, user = request.user)
		now = datetime.now()
		queryset = Reservation.objects.all().filter(owner = owner,endTime__gte = now).order_by('startTime')

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


#returns the list of passed reservations for the logged in carowner
class PassedReservationListCarOwner(generics.ListAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(CarOwner, user = request.user)
		now = datetime.now()
		queryset = Reservation.objects.all().filter(owner = owner,endTime__lte = now).order_by('startTime')

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


#Search through parkings by parkingName and location using query params search 
class ParkingSearch(generics.ListAPIView):
	queryset = Parking.objects.all().filter(validationStatus = "V")
	serializer_class = ParkingSerializer
	pagination_class = CarOwnerPagination
	filter_backends = [filters.SearchFilter,filters.OrderingFilter]
	search_fields = ['parkingName', 'location']
	ordering_fields = '__all__'

	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		min_price = request.GET.get('min_price', 0)
		max_price = request.GET.get('max_price', queryset.aggregate(max_price=Max('pricePerHour')).get('max_price'))
		has_capacity = bool(int(request.GET.get('has_capacity', 0)))

		queryset = queryset.filter(pricePerHour__gte=min_price, pricePerHour__lte=max_price)

		if has_capacity:
			current_period_ids = PeriodsList.get_current_period_ids_if_has_capacity()
			queryset.filter(id__in=current_period_ids)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


#Add credit to carowner
class AddCredit(generics.UpdateAPIView):
	queryset = CarOwner.objects.all()
	serializer_class = CarOwnerSerializer
	
	def put(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', True)
		instance = CarOwner.objects.get(user = request.user)

		if instance is None:
			return Response({'Error':'User was not found, token is incorrect'},status=status.HTTP_401_UNAUTHORIZED)

		amount = request.data.get('amount')
		if amount is None or amount < 0:
			return Response({'Error':'Please enter a valid amount'},status=status.HTTP_400_BAD_REQUEST)

		instance.credit = F('credit') + amount

		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)


class ReservationWithoutEndtime(generics.CreateAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	@transaction.atomic
	def create(self, request, *args, **kwargs):
		owner = get_object_or_404(CarOwner, user=request.user)
		parking = get_object_or_404(Parking, id=request.data['parkingId'])
		car = get_object_or_404(Car, id=request.data['car_id'], owner=owner)
		pay_with_credit = request.data.get('pay_with_credit', None)
		enter = request.data.get('enter', None)
		starting_period = None

		periods = Period.objects.all().filter(parking=parking)
		if enter:
			startTime = datetime.strptime(enter, "%Y/%m/%d %H:%M:%S")

			if startTime.minute >= 30:
				starting_period = get_object_or_404(Period, parking=parking, is_active=True,
													startTime__hour=startTime.hour, startTime__minute=30,
													weekDay=startTime.weekday())
			else:
				starting_period = get_object_or_404(Period, parking=parking, is_active=True,
													startTime__hour=startTime.hour, startTime__minute=0,
													weekDay=startTime.weekday())

			if starting_period.capacity == 0:
				return Response({'message': 'Parking is full in this period, try to choose another time'})
			periods.update(capacity=F('capacity') - 1)
			# creates a reserve without endtime
			tracking_code = Reservation.objects.filter(parking=parking).count()
			reserve = Reservation.objects.create(owner=owner, parking=parking, startTime=startTime,
												 trackingCode=tracking_code, car=car)
		elif request.data.get('exit'):
			periods.update(capacity=F('capacity') + 1)
			# completes the reserve with endtime
			reserve = Reservation.objects.get(id=request.data.get('reserve_id'))
			endTime = datetime.now()
			reserve.endTime = endTime
			duration = ((endTime - reserve.startTime).total_seconds()) / 60
			pricePerMin = parking.pricePerHour / 60
			cost = round(duration * pricePerMin, 1)
			if pay_with_credit:
				owner.credit = F('credit') - cost
				owner.save()
			reserve.cost = cost

			reserve.save()

		if starting_period:
			starting_period.refresh_from_db()

		partial = kwargs.pop('partial', True)
		serializer = self.get_serializer(reserve, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)

		return Response(serializer.data)


class GetMinMaxPrice(generics.RetrieveAPIView):
	queryset = Parking.objects.all()

	def retrieve(self, request, *args, **kwargs):
		min_price = Parking.objects.filter(validationStatus="V").aggregate(min_price=Min('pricePerHour')).get('min_price') or 0
		max_price = Parking.objects.filter(validationStatus="V").aggregate(max_price=Max('pricePerHour')).get('max_price') or 0

		return Response({0: min_price, 1: max_price}, status=status.HTTP_200_OK)


class AddParkingMonitor(generics.CreateAPIView):
	queryset = ParkingMonitor.objects.all()

	def create(self, request, *args, **kwargs):
		car_owner = CarOwner.objects.filter(user=request.user).first()
		if car_owner is None:
			return Response({'error': 'token eshtebah ast'}, status=status.HTTP_400_BAD_REQUEST)

		parking = Parking.objects.filter(id=request.data['parking_id']).first()
		if parking is None:
			return Response({'error': 'parking_id eshtebah ast'}, status=status.HTTP_400_BAD_REQUEST)

		ParkingMonitor.objects.create(car_owner=car_owner, parking=parking)
		return Response({'status': 'success'}, status=status.HTTP_201_CREATED)


class RecentParkings(generics.ListAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def list(self, request, *args, **kwargs):
		car_owner = get_object_or_404(CarOwner, user=request.user)
		parking_monitors = ParkingMonitor.objects.filter(car_owner=car_owner).order_by('-created')
		recent_parkings = []
		for parking_monitor in parking_monitors:
			recent_parkings.append(parking_monitor.parking.id)

		recent_parkings = list(set(recent_parkings))
		recent_parkings.reverse()

		parkings = []
		for id in recent_parkings:
			parkings.append(Parking.objects.get(id=id))

		serializer = self.get_serializer(parkings, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class MostPopularParkings(generics.ListAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def list(self, request, *args, **kwargs):
		most_popular_parking_monitors = ParkingMonitor.objects.filter().values('parking').annotate(count=Count('parking')).order_by('-count')[:5]
		most_popular_parkings = []
		for query in most_popular_parking_monitors:
			most_popular_parkings.append(Parking.objects.get(id=query.get('parking')))
		serializer = self.get_serializer(most_popular_parkings, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)