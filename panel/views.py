from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from website.models import Subscribe, ContactUs
from django.urls import reverse
from iot.models import iotApp, device, plan, apiKey

from django.contrib.auth import authenticate, login as userlogin, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
import json
from django.conf import settings
import stripe 
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.contrib.auth.hashers import make_password
import datetime
from datetime import date, timedelta
import calendar
from dateutil.relativedelta import relativedelta



def index(request):
	if request.user.is_authenticated:
		return render(request, 'panel/index.html')
	else:
	    return HttpResponseRedirect('/panel/login/')

def login(request):
	if request.user.is_authenticated:
	    return HttpResponseRedirect('/panel')
	else:
		return render(request, 'panel/login.html')

def signup(request):
	if request.user.is_authenticated:
	    return HttpResponseRedirect('/panel')
	else:
		return render(request, 'panel/signup.html')

def apps(request):
	if not request.user.is_authenticated:
	    return HttpResponseRedirect('/panel/login/')
	context = {}
	apps = list(iotApp.objects.filter(owner=request.user).values('name', 'key', 'username'))
	context['appcount'] = len(apps)
	devicecount = 0
	for app in apps:
		username = app['username']
		topics = list(device.objects.filter(username = username).values('name','topic'))
		devicecount += len(topics)
		app['topics'] = topics
	context['apps'] = apps
	
	context['devicecount'] = devicecount
	plan = list(request.user.groups.all().values('name'))[0]['name']

	maxapp = 0
	maxdevice = 0

	if plan == 'user':
		maxapp = 2
		maxdevice = 4
	elif plan == 'basic':
		maxapp = 5
		maxdevice = 25
	elif plan == 'ultimate':
		maxapp = 20
		maxdevice = 200

	context['maxapp'] = maxapp
	context['maxdevice'] = maxdevice

	return render(request, 'panel/apps.html', context)

def api(request):
	context = {}
	try:
		context['apiKey'] = list(apiKey.objects.filter(owner=request.user).values('key'))[0]['key']
	except Exception as e:
		context['apiKey'] = "No Key Found"
	return render(request, 'panel/api.html', context)

def devices(request):
	if not request.user.is_authenticated:
	    return HttpResponseRedirect('/panel/login/')
	context = {}

	apps = list(iotApp.objects.filter(owner=request.user).values('name', 'key', 'username'))
	appcount = len(apps)
	devicecount = 0
	for app in apps:
		username = app['username']
		topics = list(device.objects.filter(username = username).values('name','topic'))
		devicecount += len(topics)
	
	plan = list(request.user.groups.all().values('name'))[0]['name']

	maxapp = 0
	maxdevice = 0

	if plan == 'user':
		maxapp = 2
		maxdevice = 4
	elif plan == 'basic':
		maxapp = 5
		maxdevice = 25
	elif plan == 'ultimate':
		maxapp = 20
		maxdevice = 200




	if request.method == 'POST':
		form_type = request.POST['type']
		if form_type == 'delete-device':
			topic = request.POST['topic']
			device.objects.filter(topic = topic).delete()
			return HttpResponseRedirect('/panel/apps/')

		if form_type == 'add-device':
			name = request.POST['device_id']
			username = request.POST['username']
			username = iotApp.objects.get(username = username)
			# Potential Bug (User Can set key parameter themselve)
			key = request.POST['key']
			topic = key+"/"+name+"/#"
			if maxdevice >= devicecount:
				device.objects.create(username=username, name=name, topic=topic)
			else:
				context['error'] = "Device Limit Reached"
				
			return HttpResponseRedirect('/panel/apps/')

		if form_type == 'add-app':
			appname = request.POST['appname']
			key = uuid.uuid4()
			owner = request.user
			username = uuid.uuid4()
			password = uuid.uuid4()
			pw = make_password(password)
			if maxapp >= appcount:
				iotApp.objects.create(name=appname, key=key, username=username, password=password, pw=pw, owner=owner)
			else:
				context['error'] = "App Limit Reached"

			return HttpResponseRedirect('/panel/apps/')

		if form_type == 'delete-app':
			username = request.POST['username']
			key = request.POST['key']
			iotApp.objects.filter(username=username, key=key).delete()
			return HttpResponseRedirect('/panel/apps/')

	# res = {'error': 'Method Not Supported'}
	# return HttpResponse(json.dumps(res), content_type="application/json")

def account(request):
	if not request.user.is_authenticated:
	    return HttpResponseRedirect('/panel/login/')
	context = {}
	if request.method == 'POST':
		form_type = request.POST['type']
		if form_type == 'password':
			pwd = request.POST['password']
			repwd = request.POST['repassword']
			if pwd == repwd:
				current_user = request.user.username
				print(current_user)
				pw = make_password(pwd)
				User.objects.filter(username=current_user).update(password=pw)
				logout(request)
				user = authenticate(request, username = current_user, password = pwd)
				if user is not None:
					print('Hello')
					userlogin(request, user)
				context['password_changed'] = True
	return render(request, 'panel/account.html', context)

def deviceConnect(request):
	if not request.user.is_authenticated:
	    return HttpResponseRedirect('/panel/login/')
	context = {}
	if request.method == 'POST':
		key = request.POST['key']
		context['key'] = key
	return render(request, 'panel/connect.html', context)

def userlogout(request):
	if request.user.is_authenticated:
		logout(request)
		
	return HttpResponseRedirect('/panel')

def selectPlan(request):
	if not request.user.is_authenticated:
	    return HttpResponseRedirect('/panel/login/')
	context = {}
	userplan = list(plan.objects.filter(owner = request.user).values('name',))[0]['name']
	context['plan'] = userplan
	return render(request, 'panel/select-plan.html', context)

def pay(request):
	if not request.user.is_authenticated:
	    return HttpResponseRedirect('/panel/login/')
	elif request.method == 'POST':
		context = {}
		planName = request.POST['plan-name']
		planDuration = request.POST['plan-duration']
		price = request.POST['price']
		
		context['planName'] = planName
		context['planDuration'] = planDuration
		context['price'] = price

		context['key'] = settings.STRIPE_PUBLISHABLE_KEY 

		durationInMonth = 0

		if planDuration == '1m':
			durationInMonth = 1
		elif planDuration == '3m':
			durationInMonth = 3
		elif planDuration == '6m':
			durationInMonth = 6
		elif planDuration =='1y':
			durationInMonth = 12

		intent = stripe.PaymentIntent.create(
			amount=int(price)*100,
			currency='usd',
			description=planName,
			metadata = {
				'user': request.user,
				'plan': planName,
				'duration': durationInMonth
			}
		)

		context['clientSecret'] = intent.client_secret
		return render(request, 'panel/pay.html', context)

def signuplogin(request):
	try:
		redir = request.GET['next']
	except Exception as e:
		redir = '/panel'

	if request.method == 'POST':
		form_type = request.POST['type']
		if form_type == "login":
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username = username, password = password)
			if user is not None:
				userlogin(request, user)
				return HttpResponseRedirect(redir)
			else:
				messages.error(request, "Username / Password not correct")
				return HttpResponseRedirect('/panel/login?next='+redir)


		elif form_type == 'signup':
			username = request.POST['email']
			password = request.POST['password']
			email = request.POST['email']
			first_name = request.POST['first_name']
			

			context = {}

			context['username'] = email
			context['password'] = password
			context['email'] = email
			context['first_name'] = first_name
			


			if User.objects.filter(username=username).exists():
				messages.error(request, '"' + email + '" this email is already Registered')

			elif User.objects.filter(email = email).exists():
				messages.error(request, '"' + email + '" this email is already Registered')
			else:
				user = User.objects.create_user(username, email, password)
				user.first_name = first_name
				
				group = Group.objects.get(name='user')
				user.groups.add(group)
				user.is_staff = True
				user.save()
				plan.objects.create(name="user", owner=user)
				user_api_key = uuid.uuid4()
				apiKey.objects.create(owner=user, key=user_api_key)
				userlogin(request, user)
				return HttpResponseRedirect(redir)


		# query_string =  urlencode({'next': redir})
		# print(query_string)
		return HttpResponseRedirect('/panel/signup?next='+redir)
	else:
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('panel:panel-home'))
		else:
			return render(request, 'website/signuplogin.html', {'next': redir})

@csrf_exempt
def webhook(request):
  payload = request.body
  event = None

  try:
    event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  # Handle the event
  if event.type == 'payment_intent.succeeded':
    payment_intent = event.data.object # contains a stripe.PaymentIntent
    # Then define and call a method to handle the successful payment intent.
    # handle_payment_intent_succeeded(payment_intent)

    user = payment_intent.charges.data[0].metadata.user
    duration = payment_intent.charges.data[0].metadata.duration
    userplan = payment_intent.charges.data[0].metadata.plan

    w_user = User.objects.get(username = user)


    start_date = datetime.datetime.now()

    # days_in_month = calendar.monthrange(start_date.year, start_date.month)[int(duration)]
    # end_date = start_date + timedelta(days=days_in_month)

    end_date = start_date + relativedelta(months=+int(duration))

    plan.objects.filter(owner = w_user).delete()
    plan.objects.create(owner = w_user, expiry=end_date, name=userplan)


    group = Group.objects.get(name=userplan)
    w_user.groups.clear()
    w_user.groups.add(group)


    # student = Student.objects.get(userid = w_user)
    # course = Course.objects.get(id = course)

    # Student_Course.objects.create(student_id = student, course = course)

  elif event.type == 'payment_method.attached':
    payment_method = event.data.object # contains a stripe.PaymentMethod
    # Then define and call a method to handle the successful attachment of a PaymentMethod.
    # handle_payment_method_attached(payment_method)
  # ... handle other event types
  else:
    # Unexpected event type
    return HttpResponse(status=400)

  return HttpResponse(status=200)


