from django.db import models
from users.models import CustomUser
import datetime,time
from django.utils import timezone

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
	#True=Private,False=Public
	isPrivate=models.BooleanField(default=False)
	parkingName = models.CharField(max_length=200)
	location = models.CharField(max_length=100)
	parkingPhoneNumber = models.CharField(max_length=30)
	capacity = models.IntegerField(default=0)
	parkingPicture=models.ImageField(upload_to='parkingpictures/',blank=True)
	rating = models.FloatField(default=0)
	validationStatus = models.CharField(max_length=1, choices=CHOICES,default="I")

	def __str__(self):
		return self.parkingName

class Validation(models.Model):
	parking=models.OneToOneField(Parking,on_delete=models.CASCADE,null=True)
	nationalCode=models.CharField(max_length=10)
	validationFiles=models.FileField(upload_to='validationfiles/')
	postalCode=models.CharField(max_length=10)
	validationCode=models.IntegerField()
	time_Added = models.DateTimeField(default=datetime.datetime.now(timezone.utc))

	def ends_within_50_days(self):
		return (date.today() - self.Time_added).days 

	def __str__(self):
		return self.parking
	
