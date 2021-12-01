from django.db.models import query
from django.db.models import F
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import pytz
from rest_framework.response import Response
import parking
from parkingowner.models import Parking, ParkingOwner, Period
from parkingowner.serializers import ParkingSerializer, PeriodSerializer
from .models import  Car, CarOwner, Comment, Rate, Reservation
from users.models import CustomUser
from .pagination import CarOwnerPagination
from rest_framework import generics, pagination, serializers, status
from .serializers import CarOwnerSerializer, CarSerializer, CommentChildSerializer, CommentSerializer, ReservationSerializer
from django.db.models import Avg
import json
import requests
from datetime import date, datetime
from rest_framework.views import APIView
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
        instance = get_object_or_404(Car, id = request.data['id'], owner = owner)
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
        author = get_object_or_404(CarOwner, user = request.user)
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
        author = get_object_or_404(CarOwner, user = request.user)
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
        author = get_object_or_404(CarOwner, user = request.user)
        instance = get_object_or_404(Comment, id = request.data['id'], author = author)
        self.perform_destroy(instance)
        return Response({"message" : "Comment deleted successfully"},status=status.HTTP_204_NO_CONTENT)



#Add a reply to a comment by passing parking id and parent id
class CommentChildCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentChildSerializer

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(CarOwner, user = request.user)
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
    
    def post(self, request,*args, **kwargs):
        parking = get_object_or_404(Parking, id = request.data['id'])
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




class ReservationCreate(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        owner = get_object_or_404(CarOwner, user = request.user)
        parking = get_object_or_404(Parking, id = request.data['parkingId'])
        startTime = datetime.strptime(request.data['enter'],"%Y/%m/%d %H:%M:%S")
        endTime = datetime.strptime(request.data['exit'],"%Y/%m/%d %H:%M:%S")
        periods = self.getPeriods(startTime,endTime,parking)
        isValid = self.checkValidation(periods)
        if isValid == True:
            periods.update(capacity = F('capacity') - 1)
            serializer = ReservationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner = owner,parking=parking,startTime=startTime,endTime=endTime,cost = 1000)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        elif isValid == "Error, Closed Periods Found !":
            return Response({'message' : isValid})
        else:
            queryset = isValid
            serializer = PeriodSerializer(queryset,many = True)
            return Response(serializer.data)

    
    def getPeriods(self,startTime,endTime,parking):
        
        if startTime.minute >= 30:
            startPeriod = get_object_or_404(Period, parking = parking,startTime__hour = startTime.hour, startTime__minute = 30)
        else:
            startPeriod = get_object_or_404(Period, parking = parking,startTime__hour = startTime.hour, startTime__minute = 0)

        endPeriod = get_object_or_404(Period, parking = parking,endTime__hour = endTime.hour, endTime__minute = endTime.minute)

        periods = Period.objects.all().filter(parking = parking, index__gte = startPeriod.index, index__lte = endPeriod.index)

        return periods
        

    def checkValidation(self,periods):
        filledPeriods = periods.filter(capacity = 0)
        notActivePeriods = periods.filter(is_active = False)
        if notActivePeriods.count() != 0:
            return "Error, Closed Periods Found !"
        elif filledPeriods.count() == 0 :
            return True
        else:
            return filledPeriods


class ReservationList(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(CarOwner, user = request.user)
        queryset = Reservation.objects.all().filter(owner = owner)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)