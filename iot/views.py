from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from iot.models import iotApp, device
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
	if request.method == 'POST':
		try:
			key =  request.POST.get('key')
			print(request.headers)
			print(request.POST)
			res = list(iotApp.objects.filter(key=key).values('username', 'password', 'name'))[0]
			res['devices'] = list(device.objects.filter(username=res['username']).values('name',))
			return HttpResponse(json.dumps(res), content_type="application/json")
			
		except Exception as e:
			res = {'error': 'Wrong Credentials'}
			return HttpResponse(json.dumps(res), content_type="application/json")
	else:
		res = {'error': 'Method Not Supported'}
		return HttpResponse(json.dumps(res), content_type="application/json")