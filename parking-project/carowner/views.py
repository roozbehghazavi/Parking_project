from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.response import Response
from parkingowner.models import Parking
from parkingowner.serializers import ParkingSerializer
from .models import  Car, CarOwner
from .pagination import CarOwnerPagination
from rest_framework import generics, pagination, status
from .serializers import CarOwnerSerializer, CarSerializer
import json
import requests
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

class CarOwnerDetail(generics.RetrieveAPIView):
    # API endpoint that returns a single customer by pk.
    queryset = CarOwner.objects.all()
    serializer_class = CarOwnerSerializer


class CarOwnerUpdate(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a customer record to be updated.
    queryset = CarOwner.objects.all()
    serializer_class = CarOwnerSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        print(request.user.id)
        instance = get_object_or_404(CarOwner, user = request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    

class CarOwnerDelete(generics.RetrieveDestroyAPIView):
    # API endpoint that allows a customer record to be deleted.
    queryset = CarOwner.objects.all()
    serializer_class = CarOwnerSerializer




### Car Views


class CarCreate(generics.CreateAPIView):
    # API endpoint that allows creation of a new customer
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        owner = get_object_or_404(CarOwner, user = request.user)
        car = Car.objects.create(owner = owner)
        serializer = CarSerializer(car,data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




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

class CarDetail(generics.RetrieveAPIView):
    # API endpoint that returns a single customer by pk.
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class CarUpdate(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a customer record to be updated.
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDelete(generics.RetrieveDestroyAPIView):
    # API endpoint that allows a customer record to be deleted.
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def delete(self, request, *args, **kwargs):
        owner = get_object_or_404(CarOwner, user = request.user)
        instance = get_object_or_404(Car, id = request.data['id'], owner = owner)
        self.perform_destroy(instance)
        return Response({"message" : "Car deleted successfully"},status=status.HTTP_204_NO_CONTENT)


# Parking

class ParkingList(generics.ListAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    pagination_class = CarOwnerPagination

    def get(self, request, *args, **kwargs):
        queryset = Parking.objects.all().order_by('parkingName')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

