from  django.urls  import  path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('hotel-detail/<uid>/' , hotel_detail , name="hotel_detail"), 
    path('profile/<id>/',profile_page,name='profile'), 
    path('pay_success',pay_success,name='pay_success'),
	path('pay_cancel',pay_cancel,name='pay_cancel'),
    path('checkout_session/<hotel_name>/<hotel_price>/<user>/<checkin>/<checkout>/<rooms>/<adventure_list>/', checkout_session, name='checkout_session'),
    path('stripe_webhook/',stripe_webhook,name="stripe_webhook"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()