from django.contrib import admin

from carowner.models import Car, CarOwner, Comment, Rate

# Register your models here.


admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Rate)
admin.site.register(Comment)