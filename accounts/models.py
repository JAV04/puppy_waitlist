from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.core.mail import send_mail
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

import uuid


PICKUP_CHOICES = (
    ("drive", "Drive to NC and pick up"),
    ("fly", "Fly to NC and pick up"),
    ("delivery", "Conceirge service will deliver my puppy(fees applied)")
)

state_abbr = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
state_list = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming']
STATES_CHOICES = [(state_abbr[index],state_list[index].title()) for index in range(len(state_abbr))]   


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phonenumber = PhoneNumberField(blank=True, null=True)
    city        = models.CharField(max_length=25, default="", blank=True)
    state       = models.CharField(max_length=25, default="NC", choices=STATES_CHOICES)
    pickup_option = models.CharField(max_length=25, default="drive", choices=PICKUP_CHOICES)
    desired_size  = models.CharField(max_length = 8)
    have_allergies = models.BooleanField(default=False)
    has_shopping_link = models.BooleanField(default=False)
    is_shopping    = models.BooleanField(default=False)
    purchased_puppy = models.BooleanField(default=False)
    puppy_gender   = models.CharField(max_length = 10, default="")
    puppy_notes = models.TextField(max_length=250, default="", blank=True)
    breeder_notes = models.TextField(max_length=250, default="", blank=True)
    pin          = models.CharField(max_length = 10, default="")
    terms_agreed = models.BooleanField(default=True)

    class Meta:
        ordering=('date_joined',)

    def save(self, *args, **kwargs):
        create = True if not self.pk else False

        super(CustomUser, self).save(*args, **kwargs)

        # Access the through model directly
        
        # if not create:
        #      
                
        # super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {} :-: {} :-: {} :-: {}".format(self.first_name, self.last_name, self.email, self.date_joined.strftime("%Y-%m-%d %H:%M:%S"), self.phonenumber)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in CustomUser._meta.fields]

    def on_closed_list(self):
        for litter_request in self.likes.through.objects.filter(user=self) :
            if not litter_request.litter.is_live:
                return True
        return False

    def get_closed_list(self):
        for litter_request in self.likes.through.objects.filter(user=self) :
            if not litter_request.litter.is_live:
                return litter_request.litter.mother_name
        return "!DNE!"


class CustomerInvite(models.Model):
    email = models.CharField(max_length=100)
    pin   = models.CharField(max_length=100, default="")

    def __init__(self, *args, **kwargs):
        super(CustomerInvite, self).__init__(*args, **kwargs)
        self.pin = uuid.uuid4().hex[:10].upper()

    def __str__(self):
    	return self.email

    def save(self, *args, **kwargs):
    	if self.pk:
    		raise Exception("Cannot change a customer invite. Please delete and recreate!")

    	send_mail("Peter's Puppies :: Please Register "
    			, "waitlist.peterspuppies.com/accounts/register\nPin: {pin}".format(pin=self.pin)
    			, "postmaster@mg.peterspuppies.com"
    			, [self.email]
    			, fail_silently=False)

    	super(CustomerInvite, self).save(*args, **kwargs)


