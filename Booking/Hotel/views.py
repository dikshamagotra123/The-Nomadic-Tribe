from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Adventures, Hotel, HotelBooking)
from django.db.models import Q

def check_booking(start_date  , end_date ,uid_list , hotels):
    print(f"{uid_list=}")
    for uid in uid_list:
        hotel_bookings = HotelBooking.objects.filter(
            start_date__lte=start_date,
            end_date__gte=end_date,
            hotel__uid = uid
            )
        print(f"{hotel_bookings=}")
        hotel_room_dict={}
        for hotel in hotels:
            hotel_room_dict[hotel.hotel_name] = hotel.room_count

        if len(hotel_bookings) >= hotel.room_count:
            return False
    print(f"{hotel_room_dict=}")        
    return True
    
def home(request):
    adventure_objs = Adventures.objects.all()
    hotels_objs = Hotel.objects.all()
    hotel_uids = Hotel.objects.all().values_list('uid',flat=True)
    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    adventures = request.GET.getlist('adventures')
    checkin = request.GET.get('checkin')
    checkout= request.GET.get('checkout')
    alread_booked = None

    if checkin or checkout:
        if not check_booking(checkin, checkout, hotel_uids, hotels_objs):
            messages.warning(request, 'Some hotels are booked on these days')
            alread_booked = True


    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains = search) )

    if len(adventures):
        hotels_objs = hotels_objs.filter(adventures__adventure_name__in = adventures).distinct()

    print(f"{hotels_objs=}")
    print(f"{alread_booked=}")

    context = {'already_booked':alread_booked,'adventure_objs' : adventure_objs , 'hotels_objs' : hotels_objs , 'sort_by' : sort_by 
    , 'search' : search , 'adventures' : adventures}
    return render(request , 'Hotel/home.html' ,context)

def hotel_detail(request,uid):
    hotel_obj = Hotel.objects.all()
    print(f"{hotel_obj.room_count=}")
    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        hotel = Hotel.objects.get(uid=uid)
        uid_list = []
        uid_list.append(uid)
        if not check_booking(checkin ,checkout  , uid_list , hotel_obj):
            messages.warning(request, 'Hotel is already booked in these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        HotelBooking.objects.create(hotel=hotel , user = request.user , start_date=checkin
        , end_date = checkout , booking_type  = 'Pre Paid')
        
        messages.success(request, 'Your booking has been saved')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    return render(request , 'Hotel/hotel_detail.html' ,{
        'hotels_obj' :hotel_obj
    })

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Account not found ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username , password = password)
        if not user_obj:
            messages.warning(request, 'Invalid password ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        login(request , user_obj)
        return redirect('/')

        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request ,'Hotel/login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, 'Username already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()
        return redirect('/')

    return render(request , 'Hotel/register.html')