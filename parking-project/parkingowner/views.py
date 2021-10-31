from django.shortcuts import render
from rest_framework.views import APIView
from .models import ParkingOwner
from .serializers import ParkingOwnerSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
#Add or delete parking
class ParkingAV(APIView):
    permission_classes = [IsAuthenticated]
    #Create a parking and add it to database
    def post(self,request):
        #Create a model object
        Parkings=ParkingOwner.objects.all()
        #Call serializer
        serializer=ParkingOwnerSerializer(data=request.data)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class ParkingOwnerCreate(generics.CreateAPIView):
    # API endpoint that allows creation of a new customer
    queryset = ParkingOwner.objects.all()
    serializer_class = ParkingOwnerSerializer

class ParkingOwnerList(generics.ListAPIView):
    # API endpoint that allows customer to be viewed.
    queryset = ParkingOwner.objects.all()
    serializer_class = ParkingOwnerSerializer
class ParkingOwnerDetail(generics.RetrieveAPIView):
    # API endpoint that returns a single customer by pk.
    queryset = ParkingOwner.objects.all()
    serializer_class = ParkingOwnerSerializer


class ParkingOwnerUpdate(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a customer record to be updated.
    queryset = ParkingOwner.objects.all()
    serializer_class = ParkingOwnerSerializer

class ParkingOwnerDelete(generics.RetrieveDestroyAPIView):
    # API endpoint that allows a customer record to be deleted.
    queryset = ParkingOwner.objects.all()
    serializer_class = ParkingOwnerSerializer