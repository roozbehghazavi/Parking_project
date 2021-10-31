from rest_framework import serializers
from .models import ParkingOwner



#Seriliazer for ParkingOwner Model

class ParkingOwnerSerializer(serializers.ModelSerializer):
	role = serializers.CharField(source = 'user.role',required = False, read_only = True)
	firstName = serializers.CharField(source = 'user.firstName',required = False)
	lastName = serializers.CharField(source = 'user.lastName',required = False)
	email = serializers.EmailField(source = 'user.email',required = False, read_only = True)
	class Meta:
		model = ParkingOwner
		fields = ['id','role','email', 'firstName', 'lastName', 'parkingName', 'location', 'parkingPhoneNumber', 'capacity']
		
	def update(self, instance, validated_data):

	# * CarOwner.user Info
		try:
			user_data = validated_data.pop('user')
			user = instance.user
			user.firstName = user_data.get('firstName', user.firstName)
			user.lastName = user_data.get('lastName', user.lastName)
			user.role = user_data.get('role', user.role)
			user.save()
		except:
			pass

		# * CarOwner Info
		super().update(instance, validated_data)

		return instance
		