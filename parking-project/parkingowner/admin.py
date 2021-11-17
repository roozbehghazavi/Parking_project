from django.contrib import admin

from parkingowner.models import ParkingOwner,Parking,Validation

# Register your models here.

admin.site.register(ParkingOwner)
admin.site.register(Parking)
admin.site.register(Validation)