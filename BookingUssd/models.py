from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import logging
import random
logger = logging.getLogger(__name__)

# Create your models here.
class ChurchAdmin(models.Model):
	user = models.OneToOneField(User)
	notification_msisdn = models.CharField(max_length=20, null=True, blank=True)
	active = models.BooleanField(default=True)	

	def save(self, *args, **kwargs):
		if not self.notification_msisdn:
			self.notification_msisdn = self.user.username

		super(ChurchAdmin, self).save()		

	def __unicode__(self):
		return self.user.username

class Church(models.Model):
	admin = models.ManyToManyField(ChurchAdmin, blank=True)
	ussd_string = models.CharField(max_length=150,unique=True)
	name = models.CharField(max_length=100, default="Church Name")
	contact_details = models.TextField(max_length=150,default="You have not activated your account.\nDial *120*912*87*1# and Book a Demo appointment to activate.",blank=True)
	address = models.TextField(max_length=150,null=True,blank=True)
	banking_details = models.TextField(max_length=150,null=True,blank=True)
	booking_action_label = models.TextField(max_length=150,null=True,blank=True,default="Book Appointment")
	booking_subject_label = models.TextField(max_length=150,null=True,blank=True,default="What would you like to discuss?")
	booking_submission_message = models.TextField(max_length=150,null=True,blank=True,default="Thank you for submitting your request. We will be intouch shortly.")
	booking_message_label = models.TextField(max_length=150,null=True,blank=True,default="When and where?")
	updates_action_label = models.TextField(max_length=150,null=True,blank=True,default="Latest Updates")
	featured_update = models.ForeignKey('Update', null=True, blank=True, related_name="church_featured_update")
	active = models.BooleanField(default=True)	

	def __unicode__(self):
		return self.name	

	def save(self, *args, **kwargs):
		if not self.ussd_string:
			suffix = random.randint(10,1000)
			logger.info(settings.BASE_USSD_STRING+"*"+str(suffix)+"#")
			while Church.objects.filter(ussd_string=settings.BASE_USSD_STRING+"*"+str(suffix)+"#").exists():
				suffix += 1
			self.ussd_string = settings.BASE_USSD_STRING+"*"+str(suffix)+"#"

		super(Church, self).save()		

class Update(models.Model):
	church = models.ManyToManyField(Church)
	title = models.CharField(max_length=100)
	description = models.TextField(max_length=100)
	response = models.ForeignKey('Update',null=True,blank=True)
	url = models.TextField(max_length=1000,null=True,blank=True)
	fetch_url = models.BooleanField(default=False)
	datetime = models.DateTimeField()
	published = models.BooleanField(default=True)	
	public = models.BooleanField(default=True)	


	def __unicode__(self):
		return self.title	

class UssdSession(models.Model):
	session_id = models.CharField(max_length=150,null=True,blank=True)
	church = models.ForeignKey(Church,null=True,blank=True)
	request = models.TextField(max_length=5000)
	datetime = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)	


	def __unicode__(self):
		return str(self.session_id)