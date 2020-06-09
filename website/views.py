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


def about(request):
	return render(request, 'website/about.html')

def services(request):
	return render(request, 'website/services.html')

def contact(request):
	if request.method == 'POST':
		name = request.POST['name']
		subject = request.POST['subject']
		email = request.POST['email']
		message = request.POST['message']
		ContactUs.objects.create(name = name, email = email, subject = subject, message = message)
		context = {}
		context['sent'] = True
		return render(request, 'website/contact.html', context)

	return render(request, 'website/contact.html')

