from django.contrib import admin
from iot.models import iotApp
import uuid
import os

class iotAppAdmin(admin.ModelAdmin):
	model = iotApp
	list_display = ['name', 'key', 'username', 'password']
	fieldsets = ((None, {'fields': ('name',)}), )

	def save_model(self, request, obj, form, change):
		obj.key = uuid.uuid4()
		obj.owner = request.user
		obj.username = uuid.uuid4()
		obj.password = uuid.uuid4()
		obj.save()

	def get_queryset(self, request):
		qs = super(iotAppAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			return qs.filter(owner = request.user)



admin.site.register(iotApp, iotAppAdmin)