from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from .models import Car, ParkingOwner
from rest_framework import generics, status
from .serializers import CarSerializer, ParkingOwnerSerializer
import json
import requests
# Create your views here.


class CarCreate(generics.CreateAPIView):
    # API endpoint that allows creation of a new customer
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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

class ParkingOwnerCreate(generics.CreateAPIView):
    queryset = ParkingOwner.objects.all()
    serializer_class = ParkingOwnerSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)