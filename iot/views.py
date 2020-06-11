from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from iot.models import iotApp
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
	print("Hello")
	if request.method == 'POST':
		try:
			key =  request.POST.get('key')
			res = list(iotApp.objects.filter(key=key).values('username', 'password'))[0]
			return HttpResponse(json.dumps(res), content_type="application/json")
			
		except Exception as e:
			res = {'error': 'Wrong Credentials'}
			return HttpResponse(json.dumps(res), content_type="application/json")
	else:
		res = {'error': 'Method Not Supported'}
		return HttpResponse(json.dumps(res), content_type="application/json")