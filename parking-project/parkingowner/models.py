from django.db import models
from users.models import CustomUser

# Create your models here.


#Parking Owner Model

class ParkingOwner(models.Model):
	user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
	NationalCode=models.IntegerField(default=0,blank=True)

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
	likesCount = models.IntegerField(default=0)

	def __str__(self):
		return self.parkingName