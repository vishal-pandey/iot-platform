from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from django.conf import settings

from iot.models import iotApp, device, plan, apiKey
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def error(msg):
	return {"error": msg}

def checkKey(request):
	if request.method == 'POST':
		try:
			key = request.POST['key']
			isAvailable = list(apiKey.objects.filter(key=key).values('owner'))
			if len(isAvailable) > 0:
				return isAvailable[0]['owner']
			else:
				return JsonResponse(error("Wrong Credentials"))
		except Exception as e:
			return JsonResponse(error("Api Key Not Found"))
	else:
		return JsonResponse(error("Method Not Allowed"))

@csrf_exempt
def index(request):
	
	owner = checkKey(request)
	if owner != None:
		res = {
			"endpoints": [
				"https://airtrik.com/api/apps/",
				"https://airtrik.com/api/devices/"
			]
		}
		return JsonResponse(res)
	else:
		return checkKey(request)

@csrf_exempt
def apps(request, k=""):
	owner = checkKey(request)
	if type(owner) != type(JsonResponse({})):
		res = error("Something Went Wrong!!!")
		if k == "":
			res = apps_options
		elif k == "get":
			try:
				id = request.POST['id']
				try:
					res = list(iotApp.objects.filter(owner=owner, id=id).values("id", "name"))[0]
				except Exception as e:
					res = error("app not found")
			except Exception as e:
				apps = []
				for i in list(iotApp.objects.filter(owner=owner).values("id", "name")):
					apps.append(i)
				res = {
					"apps": apps
				}

		elif k == 'delete':
			try:
				id = request.POST['id']
				try:
					list(iotApp.objects.filter(owner=owner, id=id).values("id", "name"))[0]
					iotApp.objects.filter(owner=owner, id=id).delete()
					res = {"success": "App with id "+id+" and all associated devices are Deleted"}
				except Exception as e:
					res = error("app not found")
			except Exception as e:
				res = error("provide id of the app to delete")

		elif k == 'create':
			try:
				appname = request.POST['app_name']
				key = uuid.uuid4()
				username = uuid.uuid4()
				password = uuid.uuid4()
				pw = make_password(password)
				owner_ob = User.objects.get(pk=owner)
				created_app = iotApp.objects.create(name=appname, key=key, username=username, password=password, pw=pw, owner=owner_ob)
				res = {
						"id": created_app.id,
						"name": created_app.name
					}
			except Exception as e:
				res = error("parameter app_name is required")

		return JsonResponse(res)
	else:
		return checkKey(request)

@csrf_exempt
def devices(request, k=""):
	owner = checkKey(request)
	if type(owner) != type(JsonResponse({})):
		res = error("Something Went Wrong!!!")
		if k == "":
			res = devices_options
		elif k == "get":
			try:
				app_id = request.POST['app_id']
				try:
					device_id = request.POST['device_id']

					usernames = []
					for i in list(iotApp.objects.filter(owner=owner, id=app_id).values('username')):
						usernames.append(i['username'])

					try:
						res = list(device.objects.filter(username__in=usernames, id=device_id).values('id', 'name'))[0]
					except Exception as e:
						res = error("device not found")

				except Exception as e:
					usernames = []
					for i in list(iotApp.objects.filter(owner=owner, id=app_id).values('username')):
						usernames.append(i['username'])

					app_devices = []
					for i in list(device.objects.filter(username__in=usernames).values('id', 'name')):
						app_devices.append(i)

					if len(usernames) == 0:
						res = error("App Not Found")
					else:
						res = {'devices': app_devices}



			except Exception as e:
				res = error("parameter app_id is required")

		elif k == 'delete':
			try:
				app_id = request.POST['app_id']
				try:
					device_id = request.POST['device_id']

					usernames = []
					for i in list(iotApp.objects.filter(owner=owner, id=app_id).values('username')):
						usernames.append(i['username'])

					try:
						dev = list(device.objects.filter(username__in=usernames, id=device_id).values('id', 'name'))[0]
						device.objects.filter(username__in=usernames, id=device_id).delete()
						res = {"success": "device with id = "+device_id+" deleted successfully."}
					except Exception as e:
						res = error("device not found")

				except Exception as e:
					res = error("parameter device_id is required")



			except Exception as e:
				res = error("parameter app_id is required")

		elif k == 'create':
			try:
				app_id = request.POST['app_id']
				try:
					device_name = request.POST['device_name']
					try:
						theapp = list(iotApp.objects.filter(owner=owner, id=app_id).values('id', 'username', 'key'))[0]
						username = iotApp.objects.get(pk=theapp['id'])
						app_key = theapp['key']
						topic = app_key+"/"+device_name+"/#"

						created_device = device.objects.create(username=username, name=device_name, topic=topic)
						res = {
							'id': created_device.id,
							'name': created_device.name
						}

					except Exception as e:
						res = error("app not found")
				except Exception as e:
					res = error("parameter device_name is required")

			except Exception as e:
				res = error("parameter app_id is required")


		return JsonResponse(res)
	else:
		return checkKey(request)

apps_options = {
	"options": [
		{
			"endpoint": "https://airtrik.com/api/apps/get/",
			"description": "Get the list of apps",
			"method": "post",
			"parameters": {
				"key": "Airtrik Api Key",
				"id": "Id of the app to get (Optional)"
			},
			"response": "App Detail or List of Apps Present",
		},
		{
			"endpoint": "https://airtrik.com/api/apps/delete/",
			"description": "Delete the selected app",
			"method": "post",
			"parameters": {
				"key": "Airtrik Api Key",
				"id": "Id of the app to get"
			},
			"response": "success or error",
		},
		{
			"endpoint": "https://airtrik.com/api/apps/create/",
			"description": "Cerate New App",
			"method": "post",
			"parameters": {
				"key": "Airtrik Api Key",
				"name": "App Name",
			},
			"response": "Created App with app_id  and name",
		},
	]
}

devices_options = {
	"options": [
		{
			"endpoint": "https://airtrik.com/api/devices/get/",
			"description": "Get the list of devices of certain device",
			"method": "post",
			"parameters": {
				"key": "Airtrik Api Key",
				"app_id": "Id of the app of which devices to fetch.",
				"device_id": "Device id to get (Optional)"
			},
			"response": "Device detail or List of Devices Present present inside an app.",
		},
		{
			"endpoint": "https://airtrik.com/api/devices/delete/",
			"description": "Delete the selected device in side an app",
			"method": "post",
			"parameters": {
				"key": "Airtrik Api Key",
				"app_id": "Id of the app of which devices to fetch.",
				"device_id": "Device id to get (Optional)"
			},
			"response": "success or error",
		},
		{
			"endpoint": "https://airtrik.com/api/devices/create/",
			"description": "Cerate New App",
			"method": "post",
			"parameters": {
				"key": "Airtrik Api Key",
				"name": "App Name",
			},
			"response": "Created App with app_id  and name",
		},
	]
}

