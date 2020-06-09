from django.db import models
from django.contrib.auth.models import User



class iotApp(models.Model):
	name = models.CharField(blank=False, max_length=255)
	key = models.CharField(blank=False, max_length=255)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	username = models.CharField(blank=True, max_length=255, null=True)
	password = models.CharField(blank=True, max_length=255, null=True)	
	def __str__(self):
		return self.name
