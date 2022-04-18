import email
from random import randint
# from selectors import EpollSelector
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.response import Response
from .models import CustomUser, OTPValidation
from rest_framework import generics, status
from .serializers import CustomUserSerializer, OTPValidationSerializer
import json
import requests
from rest_auth.views import LoginView
from rest_framework.views import APIView
from django.conf import settings
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from datetime import date, datetime, timedelta
# Create your views here.


class CustomUserUpdate(generics.RetrieveUpdateAPIView):
	# API endpoint that allows a customer record to be updated.
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		instance = get_object_or_404(CustomUser, id = request.user.id)
		serializer = self.get_serializer(instance, data=request.data, partial=partial)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			# If 'prefetch_related' has been applied to a queryset, we need to
			# forcibly invalidate the prefetch cache on the instance.
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)

#Return user Role by token
class UserRole(generics.RetrieveAPIView):
	def get(self, request, *args, **kwargs):
		user = get_object_or_404(CustomUser, auth_token = request.auth)
		serializer=CustomUserSerializer(user)
		return Response(serializer.data['role'])
		
#Return user role alongside with token 
class CustomLoginView(LoginView):
	def get_response(self):
		data = {
				'role': self.user.role,
			}
		orginal_response = super().get_response()
		orginal_response.data.update(data)
		return orginal_response

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class PhonenumberOTP(APIView):
	queryset = OTPValidation.objects.all()
	serializer_class = OTPValidationSerializer

	def post(self, request, *args, **kwargs):
		user = get_object_or_404(CustomUser,phoneNumber=request.data['phoneNumber'])
		token=randint(11111,99999)
		print(token)
		#Call serializer
		serializer=OTPValidationSerializer(data=request.data)

		#Save data if it's valid
		if(serializer.is_valid()):
			serializer.save(user=user,token=token)
			data = {'from': '50004001885294', 'to': request.data['phoneNumber'] , 'text': 'کد احراز هویت شما: '+ str(token)+'\n'+'otp'}
			response = requests.post('https://console.melipayamak.com/api/send/simple/7557787143184d838512628417a5001f', json=data)

			return Response({"message" : "Token is sent successfully"})

		#Shows error if it's not valid
		else:
			return Response(serializer.errors)
	
	def get(self,request,*args,**kwargs):
		user = get_object_or_404(CustomUser,id=request.user.id)
		otp = OTPValidation.objects.all().filter(user=request.user).latest('id')
		time=datetime.now()-otp.time_creation

		print(time.total_seconds())

		if(time.total_seconds()<120):
			if(otp.token==request.GET['token']):
				user = get_object_or_404(CustomUser,id=request.user.id)
				user.is_verified=True
				user.save()
				return Response({"message" : "Token is valid"})
			else:
				return Response({"message" : "Invalid Token"})

		if(time.total_seconds()>120):
			otp=get_object_or_404(OTPValidation,user=request.user).delete()
			return Response({"message" : "Token is expired"})


		