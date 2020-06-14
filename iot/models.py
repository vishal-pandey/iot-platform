from django.db import models
from django.contrib.auth.models import User



class iotApp(models.Model):
	name = models.CharField(blank=False, max_length=255)
	key = models.CharField(blank=False, max_length=255)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	username = models.CharField(blank=True, max_length=255, null=True, unique=True)
	password = models.CharField(blank=True, max_length=255, null=True)
	pw = models.CharField(blank=True, max_length=128, null=True)
	super = models.SmallIntegerField(default=0)
	def __str__(self):
		return self.name

class device(models.Model):
	username = models.ForeignKey(iotApp, to_field='username',on_delete=models.CASCADE, db_column='username', null=True, blank=True)
	name = models.CharField(blank=False, max_length=255)
	topic = models.CharField(blank=False, max_length=255)
	rw = models.SmallIntegerField(default=1)
	def __str__(self):
		return self.name