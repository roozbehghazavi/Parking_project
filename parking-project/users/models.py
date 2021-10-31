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
	firstName = models.CharField(max_length=100,null=True,blank=True)
	lastName = models.CharField(max_length=100,null=True,blank=True)
	email = models.EmailField(_('email address'), unique=True)
	date_joined = models.DateTimeField(default=timezone.now)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()
	

	def __str__(self):
		return self.email

