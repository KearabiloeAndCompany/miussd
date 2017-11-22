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
	ussd_string = models.CharField(max_length=150,unique=True)
	name = models.CharField(max_length=100, default="Church Name")
	contact_details = models.TextField(max_length=150,null=True,blank=True)
	address = models.TextField(max_length=150,null=True,blank=True)
	banking_details = models.TextField(max_length=150,null=True,blank=True)
	booking_action_label = models.TextField(max_length=150,null=True,blank=True,default="Book Appointment")
	booking_subject_label = models.TextField(max_length=150,null=True,blank=True,default="What would you like to discuss?")
	booking_submission_message = models.TextField(max_length=150,null=True,blank=True,default="Thank you for submitting your request. We will be intouch shortly.")
	booking_message_label = models.TextField(max_length=150,null=True,blank=True,default="When and where?")
	updates_action_label = models.TextField(max_length=150,null=True,blank=True,default="Latest Updates")
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

class UssdSession(models.Model):
	session_id = models.CharField(max_length=150,null=True,blank=True)
	church = models.ForeignKey(Church,null=True,blank=True)
	request = models.CharField(max_length=500)
	datetime = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)	


	def __unicode__(self):
		return str(self.session_id)