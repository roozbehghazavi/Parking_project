from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


# User Authentication Model

class User(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)
	name = models.CharField(max_length=100,null=True)
	phoneNumber = models.CharField(max_length=30,null=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()
	

	def __str__(self):
		return self.email



#Parking Owner Model

class ParkingOwner(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	parkingName = models.CharField(max_length=200)
	location = models.CharField(max_length=100)
	parkingPhoneNumber = models.CharField(max_length=30)
	capacity = models.IntegerField()


# Car Model

class Car(models.Model):
	name = models.CharField(max_length=100)
	owner = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
	pelak = models.CharField(max_length=30)
	color = models.CharField(max_length=100)
	

	def __str__(self):
		return self.pelak


		



