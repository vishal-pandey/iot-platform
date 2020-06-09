from django.db import models



class Subscribe(models.Model):
	email = models.EmailField(blank=False)
	added_on = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.email


class ContactUs(models.Model):
	name = models.CharField(blank=True, max_length=255)
	email = models.CharField(blank=True, max_length=255)
	subject = models.CharField(blank=True, max_length=255)
	message = models.TextField(blank=True)

	class Meta:
		verbose_name = "Contact Us"
		verbose_name_plural = "Contact Us"


