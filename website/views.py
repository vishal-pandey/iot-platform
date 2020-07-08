from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from website.models import Subscribe, ContactUs
from django.urls import reverse
# Create your views here.


def index(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		print(email)
		s = Subscribe()
		s.email = email
		s.save()
		return HttpResponseRedirect(reverse('website:home'))
	else:

		context = {}	
		return render(request, 'website/index.html', context)



def documentation(request):
	return render(request, 'website/documentation.html')


def pricing(request):	return render(request, 'website/pricing.html')


def support(request):
	return render(request, 'website/support.html')


def template(request):
	return render(request, 'website/template.html')

def ppolicy(request):
	return render(request, 'website/privacy.html')