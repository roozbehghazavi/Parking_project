from django.shortcuts import render
from django.http import HttpResponse
from .models import Car
from rest_framework import generics
from .serializers import CarSerializer

# Create your views here.


class CarCreate(generics.CreateAPIView):
    # API endpoint that allows creation of a new customer
    queryset = Car.objects.all()
    serializer_class = CarSerializer


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