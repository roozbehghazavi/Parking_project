from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):

	class Meta:
		model = Car 
		fields = ['id','name','email','password1','password2', 'pelak', 'color']



