from django.db.models import fields
from rest_framework import serializers
from .models import Car , User , ParkingOwner

class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car 
        fields = ['id','name','email','password1','password2', 'pelak', 'color']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phoneNumber']

class ParkingOwnerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParkingOwner
        fields = ['id', 'user', 'parkingName', 'location', 'parkingPhoneNumber', 'capacity']
