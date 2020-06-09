from django.contrib import admin
from website.models import Subscribe, ContactUs

class SubscribeAdmin(admin.ModelAdmin):
	model = Subscribe
	list_display = ['email', 'added_on']

class ContactUsAdmin(admin.ModelAdmin):
	model = ContactUs
	list_display = ['name', 'email', 'subject', 'message']


admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(ContactUs, ContactUsAdmin)