
from django.contrib.auth.models import User
from django.db import models
import uuid
from django.apps import AppConfig

class Adventures(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    adventure_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.Adventures
    class Meta:
        verbose_name_plural = "Adventures"

class Amenities(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name
    class Meta:
        verbose_name_plural = "Amenities"



class Hotel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    hotel_name= models.CharField(max_length=100)
    hotel_price = models.IntegerField()
    description = models.TextField()
    adventures = models.ManyToManyField(Adventures)
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)
    review = models.IntegerField(default=7)

    def __str__(self) -> str:
        return self.hotel_name
    


class HotelImage(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    hotel= models.ForeignKey(Hotel ,related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="hotels")



class HotelBooking(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    hotel= models.ForeignKey(Hotel  , related_name="hotel_bookings" , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_bookings" , on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_type= models.CharField(max_length=100,choices=(('Pre Paid' , 'Pre Paid') , ('Post Paid' , 'Post Paid')))

    def __str__(self) -> str:
        return self.hotel.hotel_name
    
