
from django.contrib.auth.models import User
from django.db import models
import uuid
from django.apps import AppConfig


# class BaseModel(models.Model):
#     uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
#     created_at = models.DateField(auto_now_add=True)
#     updated_at = models.DateField(auto_now_add=True)

#     class Meta:
#         abstract = True # Since it is a BaseModel, hence abstract = True


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
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)

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
