from Booking.env_settings import BASE_DIR
import os

STATIC_URL = '/static/'

STATIC_DIR = os.path.join(BASE_DIR , "static")

STATICFILES_DIRS = [STATIC_DIR]

MEDIA_ROOT =  os.path.join(BASE_DIR, 'static') 
MEDIA_URL = '/media/'
