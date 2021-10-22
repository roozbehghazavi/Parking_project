from rest_framework import serializers
from .models import Car , CustomUser

class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car 
        fields = ['pk','name','driverName', 'pelak', 'color']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'spouse_name', 'date_of_birth']
