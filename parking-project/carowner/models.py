from django.db import models
from users.models import CustomUser

# Create your models here.


#Car Owner Model

class CarOwner(models.Model):
	user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
	favoriteLocations = models.CharField(max_length=100)
	profilePhoto = models.ImageField()
	cash = models.IntegerField(default=0)

	def __str__(self):
		return self.user.firstName + self.user.lastName