from re import search
from django.db.models import fields
from django.http import request
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Car, CarOwner, Comment, Reservation


#Serializer for CarOwner Model        

class CarOwnerSerializer(serializers.ModelSerializer):
	role = serializers.CharField(source = 'user.role',required = False, read_only = True)
	firstName = serializers.CharField(source = 'user.firstName',required = False)
	lastName = serializers.CharField(source = 'user.lastName',required = False)
	email = serializers.EmailField(source = 'user.email',required = False)
	profilePhoto = serializers.ImageField(source = 'user.profilePhoto', required = False)

	class Meta:
		model = CarOwner
		fields = ['id', 'role', 'firstName', 'lastName','email' , 'favoriteLocations', 'profilePhoto', 'cash']

	def update(self, instance, validated_data):

		# * CarOwner.user Info
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

		# * CarOwner Info
		super().update(instance, validated_data)

		return instance
	
		




#Serializer For Car Model

class CarSerializer(serializers.ModelSerializer):

	ownerRole = serializers.CharField(source = 'owner.user.role',required = False, read_only = True)
	ownerFirstName = serializers.CharField(source = 'owner.user.firstName',required = False)
	ownerLastName = serializers.CharField(source = 'owner.user.lastName',required = False)
	ownerEmail = serializers.EmailField(source = 'owner.user.email',required = False)
	ownerProfilePhoto = serializers.ImageField(source = 'owner.user.profilePhoto', required = False)
	pelak = serializers.CharField(min_length = 8,max_length=8)

	class Meta:
		model = Car 
		fields = ['id','ownerRole','ownerFirstName','ownerLastName','ownerEmail','ownerProfilePhoto','carName', 'pelak', 'color']
	
	
		

#Serializer for Comment model

class CommentSerializer(serializers.ModelSerializer):
	reply_count = SerializerMethodField()
	# replies = SerializerMethodField()
	author = serializers.EmailField(source = 'author.user.email',required = False)
	parkingName = serializers.CharField(source = 'parking.ParkingName',required = False)


	class Meta:
		model = Comment
		fields = ['id','content','dateAdded','author','parkingName','reply_count','parent']

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children.count()
		return 0

	# def get_replies(self, obj):
	# 	if obj.is_parent:
	# 		return CommentChildSerializer(obj.children, many=True).data
	# 	return None


#Serializer for children of a parent comment

class CommentChildSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('author', 'content', 'id','parent')

    def get_author(self, obj):
        return obj.author.user.email



class ReservationSerializer(serializers.ModelSerializer):

	owner_id = serializers.IntegerField(source = "owner.id",required = False)
	parking_id = serializers.IntegerField(source = "parking.id",required = False)
	startTime = serializers.DateTimeField(required = False)
	endTime = serializers.DateTimeField(required = False)


	class Meta:
		model = Reservation
		fields = ('id','owner_id', 'parking_id', 'startTime', 'endTime', 'cost')


