from datetime import date, datetime, timedelta
from django.db.models import fields
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import ParkingOwner,Parking, Period, Template,Validation
import pytz


#Seriliazer for ParkingOwner Model
class ParkingOwnerSerializer(serializers.ModelSerializer):
	role = serializers.CharField(source = 'user.role',required = False, read_only = True)
	firstName = serializers.CharField(source = 'user.firstName',required = False)
	lastName = serializers.CharField(source = 'user.lastName',required = False)
	email = serializers.EmailField(source = 'user.email',required = False, read_only = True)
	profilePhoto = serializers.ImageField(source = 'user.profilePhoto', required = False)
	class Meta:
		model = ParkingOwner
		fields = ['id','role','email', 'firstName', 'lastName','profilePhoto']

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

	parkingName = serializers.CharField(required = False)
	location = serializers.CharField(required = False)
	parkingPhoneNumber = serializers.CharField(required = False)
	isPrivate = serializers.BooleanField(read_only=True)

	class Meta:
		model = Parking
		fields = ['id','owner','isPrivate','parkingName','location','parkingPhoneNumber','capacity','parkingPicture','rating','validationStatus','pricePerHour']

	def create(self, validated_data):
		parking = super().create(validated_data)
		now = datetime.now()
		today = datetime.today().weekday()

		if now.minute < 30:
			startTime = datetime(year=now.year,month=now.month,day=now.day,hour=now.hour,minute=0,tzinfo=None)
		else:
			startTime = datetime(year=now.year,month=now.month,day=now.day,hour=now.hour,minute=30,tzinfo=None)

		endTime = startTime + timedelta(minutes=30)
		Period.objects.create(capacity = parking.capacity,parking=parking,startTime = startTime,endTime = endTime,weekDay = today).save()

		for i in range(335):
			startTime = startTime + timedelta(minutes=30)
			endTime = startTime + timedelta(minutes=30)
			Period.objects.create(capacity = parking.capacity,parking=parking,startTime = startTime,endTime = endTime,weekDay = startTime.weekday()).save()

		for i in range(7):
			date = datetime(year=now.year,month=now.month,day=now.day,hour=0,minute=0,tzinfo=None)
			Template.objects.create(parking=parking,weekDay = i,openAt = date,closeAt = date).save()

		return parking
	
	def validate(self, attrs):
		capacity = attrs.get('capacity')
		if capacity != None and capacity<0:
			raise serializers.ValidationError({'capacity':'capacity cant be below 0'})
		
		return attrs
			

class ValidationSerializer(serializers.ModelSerializer):
	parkingId=serializers.CharField(source='parking.id',required=False,read_only=True)
	parkingName = serializers.CharField(source = 'parking.parkingName',required = False, read_only = True)
	location = serializers.CharField(source = 'parking.location',required = False, read_only = True)
	validationStatus = serializers.CharField(source = 'parking.validationStatus',required = False, read_only = True)
	class Meta:
		model =Validation
		fields = ['id','parkingId','parkingName','location','nationalCode','postalCode','validationCode','validationFiles','validationStatus']



class PeriodSerializer(serializers.ModelSerializer):
	capacity = serializers.IntegerField(required = False)
	filledCapacity = SerializerMethodField()
	totalCapacity = SerializerMethodField()
	parking_id = serializers.IntegerField(source = "parking.id",required = False)
	startTime = serializers.DateTimeField(required = False)
	endTime = serializers.DateTimeField(required = False)

	class Meta:
		model = Period
		fields = ('id','capacity','filledCapacity','totalCapacity','parking_id','duration','startTime','endTime','is_active','weekDay')
	
	def get_filledCapacity(self,obj):
		return obj.parking.capacity - obj.capacity
	
	def get_totalCapacity(self,obj):
		return obj.parking.capacity
	



class TemplateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Template
		fields = ('id','parking','openAt','closeAt','weekDay')