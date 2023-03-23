import stripe
from .forms import profileForm
from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from .models import (Adventures, Hotel, HotelBooking)
from django.db.models import Q
from Booking.stripe_settings import *
stripe.api_key = STRIPE_SECRET_KEY
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

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
		print("\nI am in search\n") # Q objects is for oring the hotel_objs.
		hotels_objs = hotels_objs.filter(
			Q(hotel_name__icontains = search) |
			Q(description__icontains = search) ) # https://books.agiliq.com/projects/django-orm-cookbook/en/latest/query_relatedtool.html

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
		price = request.POST.get('price')
		print(f"{price=}")
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
			return redirect(f'/checkout_session/{selected_hotel.hotel_name}/{price}/{request.user}/{checkin}/{checkout}/{rooms}/{adventure_list}')
			# messages.success(request, 'Your booking has been saved')
			# return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	
	return render(request , 'Hotel/hotel_detail.html' ,{
		'hotel_booking_objs':hotel_booking_objs,
	})

@login_required
def profile_page(request,id):
	user_obj = User.objects.get(id=id)
	form = profileForm()
	booking_objs = HotelBooking.objects.filter(user=user_obj)
	# pop_up = request.GET.get('pop_up')
	if request.method == 'POST':
		delete_booking = request.POST.get('delete')
		update_user = request.POST.get('update')
		# print(f"{delete_booking=}")
		if update_user:
			form = profileForm(data=request.POST, instance=request.user)
			if form.is_valid():
				form.save()
				messages.warning(request, 'User Updated Successfully')
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		if delete_booking:
			HotelBooking.objects.get(uid=delete_booking).delete()
			messages.warning(request, 'Booking Deleted Successfully')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		form = profileForm(instance=request.user)

	context = {'user_obj':user_obj,'booking_objs': booking_objs,'form':form}	
	return render(request,"Hotel/profile.html",context)

def pay_success(request):
	# session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
	session_id = request.GET.get('session_id')
	# customer = stripe.Customer.retrieve(session.customer)
	line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
	return render(request,'success.html')


def pay_cancel(request):
	return render(request,'cancel.html')


def checkout_session(request,hotel_name,hotel_price,user,checkin,checkout,rooms,adventure_list):
	user = User.objects.get(username=user)
	session=stripe.checkout.Session.create(
		payment_method_types=['card'],
		metadata= {
			'hotel_name':hotel_name,
			'price':int(hotel_price)*100,
			'rooms':rooms,
			'user':user,
			'checkin':checkin,
			'checkout':checkout,
			'adventure_list':adventure_list,
		},
		line_items=[
			{
		  'price_data': {
			'currency': 'cad',
			'product_data': {
			  'name': hotel_name,
			},
			'unit_amount': int(hotel_price)*100,
		  },
		  'quantity': 1,
		}],
		mode='payment',
		success_url=f'http://127.0.0.1:8000/profile/{user.id}/',
		cancel_url='http://127.0.0.1:8000/pay_cancel',
		client_reference_id=hotel_name
	)
	return redirect(session.url, code=303)

@csrf_exempt
def stripe_webhook(request):
	print('WEBHOOK!')
	# You can find your endpoint's secret in your webhook settings
	endpoint_secret = 'whsec_db71ef2c0d5ca4375c4f63f883530e16e84492cb75edbc26fea9fd54d7059377'

	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None

	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, endpoint_secret
		)
	except ValueError as e:
		# Invalid payload
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		return HttpResponse(status=400)

	# Handle the checkout.session.completed event
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
		# print(f"{session['metadata']=}")
		metadata = session['metadata']
		hotel = Hotel.objects.get(hotel_name=metadata['hotel_name'])
		user = User.objects.get(username=metadata['user'])
		hotel_booking_obj = HotelBooking.objects.create(hotel=hotel , user = user , 
										start_date=metadata['checkin'], end_date = metadata['checkout'] ,
										room_count=int(metadata['rooms']), 
										booking_type  = 'Pre Paid',
										booking_price=int(metadata['price'])/100,
										adventures_booked=metadata['adventure_list'])
		print(f'{hotel_booking_obj=}')


	return HttpResponse(status=200)

def about(request):
	return render(request,"Hotel/about.html")