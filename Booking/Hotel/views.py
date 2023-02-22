from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Adventures, Hotel, HotelBooking)
from django.db.models import Q

def check_booking(start_date,end_date,hotels):
    
    uid_list = hotels.values_list('uid',flat=True)
    booked_hotels_id_list = []

    hotel_bookings = HotelBooking.objects.filter(
        start_date__lte = start_date,
        end_date__gte=end_date,
        hotel__uid__in = uid_list)
    
    for booking in hotel_bookings:
        if booking.rooms_left <= 0:
            booked_hotels_id_list.append(booking.hotel.uid)


    
    print(f"\n{booked_hotels_id_list=}\n")
        
    available_hotels_list = Hotel.objects.all().exclude(uid__in=booked_hotels_id_list)   
        
    print(f"\n{available_hotels_list=}\n")

    return available_hotels_list ,booked_hotels_id_list
    
def home(request):
    adventure_objs = Adventures.objects.all()
    hotels_objs = Hotel.objects.all()
    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    adventures = request.GET.get('adventures')
    checkin = request.GET.get('checkin')
    checkout= request.GET.get('checkout')
    
    print(checkin,checkout)
    alread_booked = None
    hotel_booking_objs = None

    if checkin or checkout:
        available_hotels_list ,booked_hotels_list = check_booking(checkin, checkout, hotels_objs)
        if len(available_hotels_list) == 0:
            messages.warning(request, 'Some hotels are booked on these days')
        else:
            hotels_objs = available_hotels_list
            hotel_booking_objs = HotelBooking.objects.filter(start_date__lte = checkin,
                                                            end_date__gte=checkout,
                                                            )


    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
            print(f"\nSort-By: {hotels_objs=}\n")
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')
            print(f"Sort-By: {hotels_objs=}")

    if search:
        print("\nI am in search\n")
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains = search) )

    if adventures:
        print(f"\nI am in adventure {adventures}\n")
        print(f"Adventure: {hotels_objs=}")
        if len(adventures):
            
            hotels_objs = hotels_objs.filter(adventures__adventure_name = adventures).distinct()
            print(f"Adventure later: {hotels_objs=}")

    print(f"Final : {hotels_objs=}")
    # print(f"Hotel_booking : {hotel_booking_objs=}")

    context = {'already_booked':alread_booked,'adventure_objs' : adventure_objs , 'hotels_objs' : hotels_objs , 'sort_by' : sort_by , 'search' : search , 'adventures' : adventures, 'checkin': checkin, 'checkout': checkout,'hotel_booking_objs':hotel_booking_objs}
    return render(request , 'Hotel/home.html' ,context)

def hotel_detail(request,uid):
    hotel_booking_objs = Hotel.objects.filter(uid=uid)
    if request.method == 'POST':
        user = request.user.id
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        rooms = request.POST.get('rooms')
        adventure_list = request.POST.getlist('adventures')
        price = request.POST.get('hotel_price')
        hotel = Hotel.objects.filter(uid=uid)

        try:
            hotel_booking_obj = HotelBooking.objects.get(hotel__uid=uid, start_date=checkin,end_date=checkout,user=user)
        except:
            hotel_booking_obj=None

        available_hotels_list ,booked_hotels_list = check_booking(checkin, checkout, hotel)
        
        try:
            selected_hotel = available_hotels_list.get(uid=uid)
        except:
            selected_hotel=None
        

        if len(booked_hotels_list) > 0:
            messages.warning(request, 'Hotel is already booked on these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif hotel_booking_obj and hotel_booking_obj.rooms_left < int(rooms):
            messages.warning(request, 'There are not enough rooms available in this hotel')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            HotelBooking.objects.create(hotel=selected_hotel , user = request.user , 
                                        start_date=checkin, end_date = checkout ,
                                        room_count=rooms, 
                                        booking_type  = 'Pre Paid',
                                        booking_price=int(price),
                                        adventures_booked=adventure_list)
            messages.success(request, 'Your booking has been saved')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return render(request , 'Hotel/hotel_detail.html' ,{
        'hotel_booking_objs':hotel_booking_objs,
    })

def profile_page(request,id):
    user_obj = User.objects.get(id=id)
    context = {'user_obj':user_obj}
    return render(request,"Hotel/profile.html",context)