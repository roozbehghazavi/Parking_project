from rest_framework import serializers

from parkingowner.models import ParkingOwner
from carowner.models import CarOwner
from .models import CustomUser
from rest_auth.registration.serializers import RegisterSerializer

#Serializer for CustomUser Model

class CustomUserSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomUser
		fields = ['id', 'role', 'firstName','lastName','email']



#Register Serializer for registering our users

class MyCustomUserRegistrationSerializer(RegisterSerializer):
	CHOICES = (
		('C', 'CarOwner'),
		('P', 'ParkingOwner'),
	)
	role = serializers.ChoiceField(choices=CHOICES)
	firstName = serializers.CharField(required = False)
	lastName = serializers.CharField(required = False)
	phoneNumber = serializers.CharField(required = False)
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
		user.phoneNumber = self.data.get('phoneNumber')
		user.firstName = self.data.get('firstName')
		user.lastName = self.data.get('lastName')
		user.email = self.data.get('email')
		if user.role == "P":
			parkingOwner = ParkingOwner.objects.create(user = user)
			parkingOwner.save()
		elif user.role == "C":
			carOwner = CarOwner.objects.create(user = user)
			carOwner.save()
		user.save()
		return user