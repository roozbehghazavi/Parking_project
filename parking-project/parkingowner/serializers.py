from rest_framework import serializers
from .models import ParkingOwner,Parking


#Seriliazer for ParkingOwner Model
class ParkingOwnerSerializer(serializers.ModelSerializer):
	role = serializers.CharField(source = 'user.role',required = False, read_only = True)
	firstName = serializers.CharField(source = 'user.firstName',required = False)
	lastName = serializers.CharField(source = 'user.lastName',required = False)
	email = serializers.EmailField(source = 'user.email',required = False, read_only = True)
	profilePhoto = serializers.ImageField(source = 'user.profilePhoto', required = False)
	class Meta:
		model = ParkingOwner
		fields = ['id','role','email', 'firstName', 'lastName','profilePhoto','NationalCode']

	def update(self, instance, validated_data):
		try:
			user_data = validated_data.pop('user')
			user = instance.user
			user.firstName = user_data.get('firstName', user.firstName)
			user.lastName = user_data.get('lastName', user.lastName)
			user.role = user_data.get('role', user.role)
			user.profilePhoto = user_data.get('profilePhoto', user.profilePhoto)
			user.save()
		except:
			pass
		super().update(instance, validated_data)

		return instance		

class ParkingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Parking
		fields = ['id','owner','isPrivate','parkingName','location','parkingPhoneNumber','capacity','parkingPicture']

	