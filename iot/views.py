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
		key =  request.POST.get('key')
		res = list(iotApp.objects.filter(key=key).values('username', 'password'))[0]
		return HttpResponse(json.dumps(res), content_type="application/json")
	else:
		context = {}
		return HttpResponse("Hello")
		# return render(request, 'website/index.html', context)