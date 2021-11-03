from django.contrib import admin

from parkingowner.models import ParkingOwner,Parking

# Register your models here.

admin.site.register(ParkingOwner)
admin.site.register(Parking)