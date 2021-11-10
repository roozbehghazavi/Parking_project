from django.contrib import admin

from carowner.models import Car, CarOwner

# Register your models here.


admin.site.register(CarOwner)
admin.site.register(Car)