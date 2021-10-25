from django.contrib import admin
from .models import CustomUser, ParkingOwner, Car

admin.site.register(CustomUser)
admin.site.register(ParkingOwner)
admin.site.register(Car)