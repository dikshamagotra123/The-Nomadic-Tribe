from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Adventures, Hotel, HotelBooking)
from django.db.models import Q

def check_booking(start_date  , end_date ,uid_list , hotels):
    print(f"{uid_list=}")
    booked_hotels_list = []
    
    for uid in uid_list:
        booked_hotel = HotelBooking.objects.filter(
            start_date__lte=start_date,
            end_date__gte=end_date,
            hotel__uid = uid
            )
        
        if booked_hotel:    
            for obj in booked_hotel:
                booked_hotels_list.append(obj.hotel)
    print(f"\n{booked_hotels_list=}\n")
        
    hotel_room_dict={}
    available_hotels_list = []    

    for hotel in hotels:
        hotel_room_dict[hotel.hotel_name] = hotel.room_count
        if hotel not in booked_hotels_list:
            available_hotels_list.append(hotel)
    
        
    print(f"\n{available_hotels_list=}\n")
    print(f"{hotel_room_dict=}")   

    return available_hotels_list ,booked_hotels_list
    
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
        available_hotels_list ,booked_hotels_list = check_booking(checkin, checkout, hotel_uids, hotels_objs)
        if len(available_hotels_list) == 0:
            messages.warning(request, 'Some hotels are booked on these days')
        else:
            hotels_objs = available_hotels_list

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
    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout= request.POST.get('checkout')
        hotel = Hotel.objects.get(uid=uid)
        uid_list = []
        uid_list.append(uid)

        available_hotels_list ,booked_hotels_list = check_booking(checkin, checkout, uid_list, hotel_obj)
        if len(booked_hotels_list) > 0:
            messages.warning(request, 'Hotel is already booked on these dates ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            HotelBooking.objects.create(hotel=available_hotels_list[0] , user = request.user , start_date=checkin, end_date = checkout , booking_type  = 'Pre Paid')
        
        messages.success(request, 'Your booking has been saved')
        # if not check_booking(checkin ,checkout  , uid_list , hotel_obj):
        #     messages.warning(request, 'Hotel is already booked in these dates ')
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
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