from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from django.contrib.auth import get_user_model
from django.core.mail import send_mail


from django.db.models import Q
from django.core.mail import send_mail

import uuid


ALLERGY_CHOICES = (
    ("no"    , "Most likely not allergy friendly coats"),
    ("maybe" , "Possibly some allergy friendly coats"),
    ("yes"   , "The most allergy friendly coats"),
)

SIZE_CHOICES = (
    ("mini"    , "Miniature (20-35 lbs)"),
    ("medium"  , "Medium (35-50 lbs)"),
    ("standard", "Standard 50+ lbs"),
    ("any"     , "All Sizes"),
)

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("either", "Either")
)


class LitterArchive(models.Model):
    mother_name = models.CharField(max_length=100, default="")
    birth_date = models.DateField(null=True, blank=True)
    user_list  = models.TextField(max_length=1500, default="")

class Litter(models.Model):
    mother_name = models.CharField(max_length=100, default="")
    birth_date      = models.DateField(null=True, blank=True)
    selection_date  = models.DateField(null=True, blank=True)
    takehome_startdate   = models.DateField(null=True, blank=True)
    takehome_enddate     = models.DateField(null=True, blank=True)
    available_count = models.IntegerField(default=0)
    male_count = models.IntegerField(default=0)
    female_count = models.IntegerField(default=0)
    size = models.CharField(max_length = 8, default="", choices=SIZE_CHOICES)
    allergy_friendly = models.CharField(max_length = 5, default="no", choices=ALLERGY_CHOICES)
    breeder_notes = models.TextField(max_length=500, default="")
    stripe_link    = models.URLField(max_length=200, default="", blank=True)
    stripe_link_pin = models.CharField(max_length=25, default="", blank=True)

    is_live     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True, db_index=True)
    likes = models.ManyToManyField(get_user_model(), related_name="likes", through="LitterRequest", blank=True)


    def save(self, *args, **kwargs):
        create = True if not self.pk else False

        super(Litter, self).save(*args, **kwargs)

        # if create:
        #     for user in get_user_model().objects.filter(first_available=True):
        #         self.likes.add(user)
        #     self.save(*args, **kwargs)

    def get_size(self):
        for size, display in SIZE_CHOICES:
            if size == self.size:
                return display

    def get_allergy_friendly(self):
        for friendly, display in ALLERGY_CHOICES:
            if friendly == self.allergy_friendly:
                return display

    def get_mother_name(self):
        return self.mother_name.title()

    def get_litter_name(self):
        return "{}'s Litter".format(self.get_mother_name)

    
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Litter._meta.fields]

    def __str__(self):
        return "{name} ({count} Interested)".format(name=self.mother_name.title(), count=self.likes.count())

class LitterRequest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    litter = models.ForeignKey(Litter, on_delete=models.CASCADE)

    def post_pass_pin(self):
        endpoint = "https://peterspuppies.com/wp-json/canine/add-pin-to-litter"
        data = {"pin": self.user.pin}
        headers = {
            "Content-Type":"application/json",
            "Accept":"application/json",
        }
        try:
            response = requests.post(url=endpoint, data=json.dumps(data), headers=headers)
            if response.ok:
                print(response.content)
            else:
                "issue"
        except requests.exceptions.Timeout:
            print("Time out")
        except json.decoder.JSONDecodeError:
            print("Response is not in json format")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def email_shopping_request(self, *args, **kwargs):

        self.post_pass_pin()

        send_mail("Peter's Puppies :: {} Shopping".format(str(self.litter))
                , "waitlist.peterspuppies.com/shop/{id} \n Shopping Pin: {pin}".format(id = self.id, pin=self.litter.stripe_link_pin)
                , "postmaster@mg.peterspuppies.com"
                , [self.user.email]
                , fail_silently=False)

    # def __init__(self, *args, **kwargs):
    #     super(LitterRequest, self).__init__(args, kwargs)
    #     self.my_field = 1



