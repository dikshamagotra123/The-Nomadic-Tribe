from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Adventures)
admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(HotelBooking)
