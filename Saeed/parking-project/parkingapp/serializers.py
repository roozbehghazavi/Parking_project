from django.db.models import fields
from rest_framework import serializers
from .models import Car , CustomUser , ParkingOwner
from rest_auth.registration.serializers import RegisterSerializer

class CarSerializer(serializers.ModelSerializer):

	class Meta:
		model = Car 
		fields = ['id','name','email','password1','password2', 'pelak', 'color']


class CustomUserSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomUser
		fields = ['id', 'role', 'phoneNumber', 'firstName','lastName','email']

class ParkingOwnerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ParkingOwner
		fields = ['id', 'user', 'parkingName', 'location', 'parkingPhoneNumber', 'capacity']

class MyCustomUserRegistrationSerializer(RegisterSerializer):
	CHOICES = (
		('C', 'CarOwner'),
		('P', 'ParkingOwner'),
	)
	role = serializers.ChoiceField(choices=CHOICES)
	firstName = serializers.CharField()
	lastName = serializers.CharField()
	phoneNumber = serializers.CharField()
	email = serializers.EmailField()

	def get_cleaned_data(self):
		super(MyCustomUserRegistrationSerializer, self).get_cleaned_data()
		return {
			'password1': self.validated_data.get('password1', ''),
			'password2': self.validated_data.get('password2', ''),
			'email': self.validated_data.get('email', ''),
			'firstName': self.validated_data.get('firstName', ''),
			'lastName': self.validated_data.get('last_name', ''),
			'role': self.validated_data.get('role',''),
			'phoneNumber': self.validated_data.get('phoneNumber',''),
		}

	def save(self, request):
		user = super().save(request)
		user.role = self.data.get('role')
		print(user.role)
		user.phoneNumber = self.data.get('phoneNumber')
		user.firstName = self.data.get('firstName')
		user.lastName = self.data.get('lastName')
		user.email = self.data.get('email')
		user.save()
		return user
