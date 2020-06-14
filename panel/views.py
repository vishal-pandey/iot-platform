from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from website.models import Subscribe, ContactUs
from django.urls import reverse
from iot.models import iotApp, device


from django.contrib.auth import authenticate, login as userlogin, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.contrib.auth.hashers import make_password





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
	context = {}
	apps = list(iotApp.objects.filter(owner=request.user).values('name', 'key', 'username'))
	for app in apps:
		username = app['username']
		topics = list(device.objects.filter(username = username).values('name','topic'))
		app['topics'] = topics
	context['apps'] = apps

	return render(request, 'panel/apps.html', context)



def devices(request):
	context = {}
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
			key = request.POST['key']
			topic = key+"/"+name+"/#"
			device.objects.create(username=username, name=name, topic=topic)
			return HttpResponseRedirect('/panel/apps/')

		if form_type == 'add-app':
			appname = request.POST['appname']
			key = uuid.uuid4()
			owner = request.user
			username = uuid.uuid4()
			password = uuid.uuid4()
			pw = make_password(password)
			iotApp.objects.create(name=appname, key=key, username=username, password=password, pw=pw, owner=owner)
			return HttpResponseRedirect('/panel/apps/')

		if form_type == 'delete-app':
			username = request.POST['username']
			key = request.POST['key']
			iotApp.objects.filter(username=username, key=key).delete()
			return HttpResponseRedirect('/panel/apps/')

	# res = {'error': 'Method Not Supported'}
	# return HttpResponse(json.dumps(res), content_type="application/json")





def account(request):
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
	context = {}
	if request.method == 'POST':
		key = request.POST['key']
		context['key'] = key
	return render(request, 'panel/connect.html', context)



def userlogout(request):
	if request.user.is_authenticated:
		logout(request)
		
	return HttpResponseRedirect('/panel')


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

