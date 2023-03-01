try:
    from Booking.env_settings import *
    from Booking.static_settings import *
    from Booking.templates_settings import *
    from Booking.database_settings import *
    from Booking.apps_settings import *
    from Booking.middleware_settings import *
    from Booking.auth_settings import *
    from Booking.locale_settings import *
    from Booking.url_settings import *
    from Booking.fixture_settings import *
    from Booking.fields_settings import *
    from Booking.stripe_settings import *
except ImportError:
    pass

SECRET_KEY = 'django-insecure-n15)bjerq(w7rl+v-=ivq2o%l4kl+em9z-69-hejs64a0tf8&u'