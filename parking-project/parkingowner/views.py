from django.shortcuts import render
from rest_framework.views import APIView
from .models import ParkingOwner,Parking,Validation
from .serializers import ParkingOwnerSerializer, ParkingSerializer,ValidationSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from django.shortcuts import get_object_or_404,get_list_or_404
from .pagination import ParkingListPagination

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
		#Call serializer
		serializer=ParkingSerializer(data=request.data)

		#Save data if it's valid
		if(serializer.is_valid()):
			serializer.save(owner=owner)
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
class ParkingDetail(generics.RetrieveAPIView):
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer
	
	def get(self, request, *args, **kwargs):
		owner = get_object_or_404(ParkingOwner, user = request.user)
		instance = get_object_or_404(Parking, id = request.data['id'], owner = owner)
		serializer = self.get_serializer(instance)
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

class Validator(generics.CreateAPIView):
	queryset=Validation.objects.all()
	serializer_class=ValidationSerializer

	def post(self,request,*args, **kwargs):		
		owner = get_object_or_404(ParkingOwner, user = request.user)
		parking = get_object_or_404(Parking,owner=owner)

		#Call serializer
		serializer=ValidationSerializer(data=request.data)

		#Save data if it's valid
		if(serializer.is_valid()):
			serializer.save(owner=owner)
			return Response(serializer.data)

		#Shows error if it's not valid
		else:
			return Response(serializer.errors)
