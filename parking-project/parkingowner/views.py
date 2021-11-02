from django.shortcuts import render
from rest_framework.views import APIView
from .models import ParkingOwner,Parking
from .serializers import ParkingOwnerSerializer, ParkingSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
#Add or delete parking
# class addParking(APIView):
# 	# permission_classes = [IsAuthenticated, IsPrivateAllowed]
# 	#Create a parking and add it to database
# 	queryset = Parking.objects.all()
# 	serializer_class = ParkingSerializer

# 	def post(self,request,*args, **kwargs):
# 		#Create a model object
# 		parking=Parking.objects.create(owner=request.user)
# 		#Call serializer
# 		serializer=ParkingSerializer(parking,data=request.data)
		
# 		if(serializer.is_valid()):
# 			serializer.save()
# 			return Response(serializer.data)
# 		else:
# 			return Response(serializer.errors)
			
class ParkingCreate(generics.CreateAPIView):
	# API endpoint that allows creation of a new customer
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer

	def create(self, request, *args, **kwargs):
		parking = Parking.objects.create(owner = request.user)
		serializer = ParkingSerializer(parking,data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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

class ParkingOwnerDelete(generics.RetrieveDestroyAPIView):
	# API endpoint that allows a customer record to be deleted.
	queryset = ParkingOwner.objects.all()
	serializer_class = ParkingOwnerSerializer