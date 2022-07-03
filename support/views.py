from django.shortcuts import render
from os import close
import pytz
from rest_framework.views import APIView
from carowner.models import Comment, Reservation
from carowner.serializers import CommentSerializer, ReservationSerializer

import parking
from support.models import Support
from support.serializers import SupportSerializer
from users.models import CustomUser
from parkingowner.models import ParkingOwner,Parking, Period, Template,Validation
from parkingowner.serializers import ParkingOwnerSerializer, ParkingSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from django.shortcuts import get_object_or_404,get_list_or_404
from parkingowner.pagination import ParkingListPagination
from django.utils import timezone
from datetime import date, datetime, timedelta
from dateutil import parser
from django.db.models import F, Q, Count
from rest_framework import viewsets
# Create your views here.

class ParkingList(generics.ListAPIView):
	pagination_class=ParkingListPagination
	queryset = Parking.objects.all()
	serializer_class = ParkingSerializer
	
	def get(self, request, *args, **kwargs):
		queryset = Parking.objects.all()

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

class ReservationListParking(generics.ListAPIView):
	queryset = Reservation.objects.all()
	serializer_class = ReservationSerializer

	def get(self, request, *args, **kwargs):
		parking = get_object_or_404(Parking,id = request.GET['parkingId'])
		queryset = Reservation.objects.all().filter(parking = parking)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


class SupportDetail(generics.RetrieveAPIView):
	# API endpoint that returns a single customer by pk.
	queryset = Support.objects.all()
	serializer_class = SupportSerializer

	def get(self, request, *args, **kwargs):
		instance = get_object_or_404(Support, user=request.user)
		serializer = self.get_serializer(instance)
		return Response(serializer.data)