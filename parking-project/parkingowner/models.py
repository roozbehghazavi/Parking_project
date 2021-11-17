from django.db import models
from users.models import CustomUser

# Create your models here.


#Parking Owner Model

class ParkingOwner(models.Model):
	user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.user.email

class Parking(models.Model):	
	owner = models.ForeignKey(ParkingOwner,on_delete=models.CASCADE,null=True)
	#True=Private,False=Public
	isPrivate=models.BooleanField(default=False)
	parkingName = models.CharField(max_length=200)
	location = models.CharField(max_length=100)
	parkingPhoneNumber = models.CharField(max_length=30)
	capacity = models.IntegerField(default=0)
	parkingPicture=models.ImageField(upload_to='parkingpictures/',blank=True)
	likes = models.IntegerField(default=0)
	isValid=models.BooleanField(default=False)

	def __str__(self):
		return self.parkingName

class Validation(models.Model):
	parking=models.OneToOneField(Parking,on_delete=models.CASCADE)
	nationalCode=models.CharField(max_length=10)
	validationFiles=models.FileField(upload_to='validationfiles/')
	postalCode=models.CharField(max_length=10)
	validationCode=models.IntegerField()

	def __str__(self):
		return self.parking
	