from django.shortcuts import render
from rest_framework.views import APIView
from .models import ParkingOwner
from .serializer import ParkingOwnerSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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

