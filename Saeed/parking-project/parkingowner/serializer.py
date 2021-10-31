from rest_framework import serializers
from .models import ParkingOwner



#Seriliazer for ParkingOwner Model

class ParkingOwnerSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ParkingOwner
		fields = ['id', 'user', 'parkingName', 'location', 'parkingPhoneNumber', 'capacity']
		