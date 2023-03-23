
from django.contrib.auth.models import User
from django.db import models
import uuid
import datetime
class Adventures(models.Model):
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True)
    adventure_name = models.CharField(max_length=100)
    adventure_description = models.TextField(max_length=250,default="Description")
    adventure_price = models.DecimalField(decimal_places=2,max_digits=4,default=50)

    def __str__(self) -> str:
        return self.adventure_name
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
    uid = models.UUIDField(default=uuid.uuid4   , editable=False , primary_key=True) # Why UUID?
    hotel_name= models.CharField(max_length=100)
    hotel_price = models.IntegerField()
    description = models.TextField()
    adventures = models.ManyToManyField(Adventures) #Why Many Many ?
    amenities = models.ManyToManyField(Amenities)
    room_count = models.IntegerField(default=10)
    review = models.DecimalField(max_digits=2,decimal_places=1)

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
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    room_count = models.IntegerField(default=1)
    booking_price = models.IntegerField(default=100 )
    adventures_booked = models.CharField(max_length=100,null=True,blank=True)
    booking_type= models.CharField(max_length=100,choices=(('Pre Paid' , 'Pre Paid') , ('Post Paid' , 'Post Paid')))
    
    def __str__(self) -> str:
        return self.hotel.hotel_name

    @property
    def rooms_left(self):
        total_rooms = self.hotel.room_count
        rooms_booked = self.room_count
        available_rooms = total_rooms - rooms_booked
        return available_rooms

    


    
