from django.db import models
from users.models import CustomUser
import datetime,time
from django.utils import timezone
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField

# Create your models here.

#Parking Owner Model

class ParkingOwner(models.Model):
	user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.user.email





class Parking(models.Model):	
	CHOICES = (
		('V', 'Valid'),
		('I', 'Invalid'),
		('P', 'Pending'),
	)
	owner = models.ForeignKey(ParkingOwner,on_delete=models.CASCADE,null=True)
	isPrivate=models.BooleanField(default=False)
	parkingName = models.CharField(max_length=200)
	location = models.CharField(max_length=100)
	parkingPhoneNumber = models.CharField(max_length=30)
	capacity = models.IntegerField(default=0)
	parkingPicture=models.ImageField(upload_to='parkingpictures/',blank=True)
	rating = models.FloatField(default=0)
	validationStatus = models.CharField(max_length=1, choices=CHOICES,default="I")
	pricePerHour = models.IntegerField(default=0)
	isAccessible=models.BooleanField(default=False)


	def __str__(self):
		return self.parkingName


class Validation(models.Model):
	parking=models.OneToOneField(Parking,on_delete=models.CASCADE,null=True)
	nationalCode=models.CharField(max_length=10)
	validationFiles=models.FileField(upload_to='validationfiles/')
	postalCode=models.CharField(max_length=10)
	validationCode=models.IntegerField()
	time_Added = models.DateTimeField(default=timezone.now)



	def __str__(self):
		return self.parking
	



class Period(models.Model):
	capacity = models.IntegerField(default=0)
	parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
	duration = models.DurationField(default=timedelta(hours=0.5))
	startTime = models.DateTimeField()
	endTime = models.DateTimeField()
	weekDay = models.IntegerField(default=0)

	is_active = models.BooleanField(default=True)


class Template(models.Model):
	parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
	openAt = models.DateTimeField()
	closeAt = models.DateTimeField()
	weekDay = models.IntegerField(default=0)


