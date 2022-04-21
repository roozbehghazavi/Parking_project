from typing_extensions import Required
from rest_framework import serializers

from parkingowner.models import ParkingOwner
from carowner.models import CarOwner
from .models import CustomUser,OTPValidation
from rest_auth.registration.serializers import RegisterSerializer

#Serializer for CustomUser Model

class CustomUserSerializer(serializers.ModelSerializer):
	CHOICES = (
		('C', 'CarOwner'),
		('P', 'ParkingOwner'),
	)
	role = serializers.ChoiceField(choices=CHOICES,required = False)
	firstName = serializers.CharField(required = False)
	lastName = serializers.CharField(required = False)
	email = serializers.EmailField(required = False)
	profilePhoto = serializers.ImageField(required = False)
	phoneNumber = serializers.CharField(required=False)
	is_verified = serializers.BooleanField(read_only=False,required=False)

	class Meta:
		model = CustomUser
		fields = ['id', 'role', 'firstName','lastName','email','profilePhoto','phoneNumber','is_verified']



#Register Serializer for registering our users

class MyCustomUserRegistrationSerializer(RegisterSerializer):
	CHOICES = (
		('C', 'CarOwner'),
		('P', 'ParkingOwner'),
	)
	role = serializers.ChoiceField(choices=CHOICES)
	firstName = serializers.CharField(required = False)
	lastName = serializers.CharField(required = False)
	email = serializers.EmailField()
	profilePhoto = serializers.ImageField(required = False)

	def get_cleaned_data(self):
		super(MyCustomUserRegistrationSerializer, self).get_cleaned_data()
		return {
			'password1': self.validated_data.get('password1', ''),
			'password2': self.validated_data.get('password2', ''),
			'email': self.validated_data.get('email', ''),
			'firstName': self.validated_data.get('firstName', ''),
			'lastName': self.validated_data.get('lastName', ''),
			'role': self.validated_data.get('role',''),
			'profilePhoto' : self.validated_data.get('profilePhoto',''),
		}

	def save(self, request):
		user = super().save(request)
		user.role = self.data.get('role')
		user.firstName = self.data.get('firstName')
		user.lastName = self.data.get('lastName')
		user.email = self.data.get('email')
		user.profilePhoto = self.data.get('profilePhoto')
		if user.role == "P":
			parkingOwner = ParkingOwner.objects.create(user = user)
			parkingOwner.save()
		elif user.role == "C":
			carOwner = CarOwner.objects.create(user = user)
			carOwner.save()
		user.save()
		return user
	
class OTPValidationSerializer(serializers.ModelSerializer):
	token = serializers.CharField(read_only=True)
	time_creation = serializers.DateTimeField(read_only=True)
	class Meta:
		model = OTPValidation
		fields = ['token','time_creation']