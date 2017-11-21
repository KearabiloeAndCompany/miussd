from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class ChurchAdmin(models.Model):
	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.user.username

class Church(models.Model):
	admin = models.ManyToManyField(ChurchAdmin)
	ussd_string = models.CharField(max_length=150,null=True)
	name = models.CharField(max_length=100, default="Church Name")
	contact_details = models.CharField(max_length=150)
	address = models.CharField(max_length=150)
	banking_details = models.CharField(max_length=150)
	featured_update = models.ForeignKey('Update', null=True, blank=True, related_name="church_featured_update")

	def __unicode__(self):
		return self.name	

class Update(models.Model):
	church = models.ManyToManyField(Church)
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	datetime = models.DateTimeField()
	published = models.BooleanField(default=True)	


	def __unicode__(self):
		return self.title	
