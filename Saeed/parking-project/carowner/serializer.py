from rest_framework import serializers
from .models import CarOwner


#Serializer for CarOwner Model        

class CarOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarOwner
        fields = ['id', 'user', 'favoriteLocations', 'profilePhoto', 'cash']