from  django.urls  import  path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('check_booking/' , check_booking),
    path('', home, name='home'),
    path('hotel-detail/<uid>/' , hotel_detail , name="hotel_detail"), 
    path('profile/<id>/',profile_page,name='profile'), 
    # path('create-checkout-session/<hotel_name>/<hotel_price>/', CreateCheckoutSessionView, name='create-checkout-session'),
    path('product-checkout-info/', ProductLandingPageView, name='landing-page'),
    path('cancel/', CancelView, name='cancel'),
    path('success/', SuccessView, name='success'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()