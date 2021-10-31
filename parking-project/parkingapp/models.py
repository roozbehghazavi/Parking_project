from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser



# Car Model

class Car(models.Model):
	name = models.CharField(max_length=100)
	owner = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)
	pelak = models.CharField(max_length=30)
	color = models.CharField(max_length=100)
	

	def __str__(self):
		return self.pelak

