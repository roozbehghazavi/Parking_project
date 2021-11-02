from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.response import Response
from .models import  Car, CarOwner
from rest_framework import generics, status
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
        car = Car.objects.create(owner = request.user)
        car.carName = request.data['carName']
        car.pelak = request.data['pelak']
        car.color = request.data['color']
        serializer = CarSerializer(car,data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CarList(generics.ListAPIView):
    # API endpoint that allows customer to be viewed.
    queryset = Car.objects.all()
    serializer_class = CarSerializer

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