from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import CustomerInvite, STATES_CHOICES, PICKUP_CHOICES
from puppies.models import SIZE_CHOICES, GENDER_CHOICES
from phonenumber_field.formfields import PhoneNumberField



class RegisterForm(UserCreationForm):

    city        = forms.CharField()
    state       = forms.ChoiceField(choices=STATES_CHOICES)
    pickup_option = forms.ChoiceField(choices=PICKUP_CHOICES)
    puppy_gender  = forms.ChoiceField(choices=GENDER_CHOICES)
    phonenumber = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}), label="Phone number", required=False)
    terms_agreed = forms.BooleanField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('pin', 'username', 'email', 'phonenumber', 'city', 'state', 'pickup_option', 'first_name', 'last_name', 'password1', 'password2', 'desired_size', 'puppy_gender','have_allergies', 'puppy_notes', 'terms_agreed')

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    phonenumber = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}), label="Phone number", required=False)
    city        = forms.CharField()
    state       = forms.ChoiceField(choices=STATES_CHOICES)
    pickup_option = forms.ChoiceField(choices=PICKUP_CHOICES)
    desired_size = forms.ChoiceField(choices=SIZE_CHOICES)
    puppy_gender = forms.ChoiceField(choices=GENDER_CHOICES)
    terms_agreed = forms.BooleanField(required=True, disabled=True)

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['terms_agreed'].widget.attrs['readonly'] = True

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'phonenumber', 'city', 'state', 'pickup_option', 'first_name', 'last_name', 'puppy_gender', 'desired_size', 'have_allergies', 'puppy_notes', "terms_agreed")
