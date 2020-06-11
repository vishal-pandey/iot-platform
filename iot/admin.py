from django.contrib import admin
from iot.models import iotApp, device
import uuid
import os
from django.contrib.auth.hashers import make_password
from pprint import pprint
from inspect import getmembers

class deviceAdmin(admin.TabularInline):
	model = device
	fieldsets = ((None, {'fields': ('name',)}), )


class iotAppAdmin(admin.ModelAdmin):
	model = iotApp
	list_display = ['name', 'key']
	# list_display = ['name', 'key', 'username', 'password', 'pw']
	fieldsets = ((None, {'fields': ('name',)}), )
	inlines = [deviceAdmin]


	def save_model(self, request, obj, form, change):
		if not change:
			obj.key = uuid.uuid4()
			obj.owner = request.user

			username = uuid.uuid4()
			obj.username = username

			self.username = username

			password = uuid.uuid4()
			obj.password = password

			obj.pw = make_password(password)
		if change:
			self.username = obj.username

		# command = "sudo mosquitto_passwd -b /etc/mosquitto/passwd "+str(username)+""+" "+str(password)+""
		# os.system(command)
		# os.system("sudo kill -HUP 18371")

		obj.save()


	def save_formset(self, request, form, formset, change):
		formset.save()
		
		for f in formset.forms:
			obj = f.instance
			# print(obj.name) 
			obj.topic = str(self.username)+"/"+obj.name+"/#"
			# pprint(getmembers(obj))
			if str(obj.name) != "":
				obj.save()



	# def save_related(self, request, obj, form, change):
	# 	username = form
	# 	print(username)
	# 	print("Hello World")
	# 	# obj.topic = username+"/"+name
	# 	obj.save()


	def get_queryset(self, request):
		qs = super(iotAppAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			self.list_display = ['name', 'key', 'username', 'password', 'pw']
			return qs
		else:
			return qs.filter(owner = request.user)



admin.site.register(iotApp, iotAppAdmin)
