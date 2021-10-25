from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

# Create your models here.


# User Authentication Model

class CustomUser(AbstractBaseUser, PermissionsMixin):
	CHOICES = (
		('C', 'CarOwner'),
		('P', 'ParkingOwner'),
	)
	role = models.CharField(max_length=1, choices=CHOICES)
	firstName = models.CharField(max_length=100,null=True)
	lastName = models.CharField(max_length=100,null=True)
	email = models.EmailField(_('email address'), unique=True)
	date_joined = models.DateTimeField(default=timezone.now)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()
	

	def __str__(self):
		return self.email



#Parking Owner Model

class ParkingOwner(models.Model):
	user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
	parkingName = models.CharField(max_length=200)
	location = models.CharField(max_length=100)
	parkingPhoneNumber = models.CharField(max_length=30)
	capacity = models.IntegerField(default=0)

	def __str__(self):
		return self.user.firstName + self.user.lastName



#Car Owner Model

class CarOwner(models.Model):
	user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
	favoriteLocations = models.CharField(max_length=100)
	profilePhoto = models.ImageField()
	cash = models.IntegerField(default=0)

	def __str__(self):
		return self.user.firstName + self.user.lastName