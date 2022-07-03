from django.db import models
from users.models import CustomUser
import datetime,time
from django.utils import timezone
from datetime import timedelta
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Support(models.Model):
	user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True)

	def __str__(self):
		return self.user.email