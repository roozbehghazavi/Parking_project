from django.db import models
from users.models import CustomUser

# Create your models here.


#Car Owner Model

class CarOwner(models.Model):
	user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
	favoriteLocations = models.CharField(max_length=100,blank=True)
	profilePhoto = models.ImageField(blank=True)
	cash = models.IntegerField(default=0,blank=True)

	def __str__(self):
		return self.user.firstName + self.user.lastName



class Car(models.Model):
	owner = models.ForeignKey(CarOwner,on_delete=models.CASCADE,null=True)
	carName = models.CharField(max_length=100)
	pelak = models.CharField(max_length=30)
	color = models.CharField(max_length=100)
	

	def __str__(self):
		return self.pelak
