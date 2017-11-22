from django.contrib import admin

# Register your models here.
from django.contrib import admin
from BookingUssd.models import *

admin.site.register(ChurchAdmin)
admin.site.register(Church)
admin.site.register(Update)
admin.site.register(UssdSession)
