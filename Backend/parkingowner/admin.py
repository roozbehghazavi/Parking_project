from django.contrib import admin

from parkingowner.models import ParkingOwner,Parking, Period,Validation

# Register your models here.

admin.site.register(ParkingOwner)
admin.site.register(Parking)
admin.site.register(Validation)
admin.site.register(Period)