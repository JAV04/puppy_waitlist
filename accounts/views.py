

from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate

from django.views import generic
from django import forms
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.shortcuts import render, redirect

from .forms import  RegisterForm, UpdateUserForm
from .models import CustomerInvite
import django.contrib.auth as auth

from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib import messages



from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# def login_request(request):
#     form = AuthenticationForm()
#     return render(request = request,
#                   template_name = "accounts/login.html",
#                   context={"form":form})




def login_view(request):
	raise Exception 
	if request.user.is_authenticated:
		return redirect('/')
	
	if request.method == "POST":
		form = AuthenticationForm(request.POST)
		

		if request.user:
			user = auth_authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
			
			if not user.is_anonymous:
				auth_login(request, user)
				messages.success(request, "Welcome, {}!".format(user.first_name.title()))
				return redirect("/")
		messages.error(request, 'Failed to login!!')
		return render(request, 'registration/login.html', {'form': form})

	else:
		form = AuthenticationForm()
		return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    auth.logout(request)
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):

	if request.user.is_authenticated:
		return redirect("/")

	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():

			user = form.save(commit=False)

			if not CustomerInvite.objects.filter(pin=user.pin).exists():
				return render(request, 'accounts/invalid.html', {'form': form})
			else:
				CustomerInvite.objects.filter(pin=user.pin).delete()

			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')

			user.set_password(password)
			user.save()

			auth_authenticate(request, username=username, password=password)
			auth_login(request, user)

			messages.success(request, "Welcome, {}, you will see litters on this page as they are posted!".format(user.first_name.title()))

			return redirect("/")


	else:
		form = RegisterForm()
	return render(request, 'registration/register.html', {'form': form})


# def profile_view(request):
#     args = {}

#     if request.method == 'POST':
        
#         form.actual_user = request.user
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('update_profile_success'))
#     else:
#         form = UpdateUser()

#     context={'form': form}
    

def profile_view(request):
	if request.method == 'POST':
		form = UpdateUserForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request,'Your profile has been updated!')
			return redirect("/")
	else:
		form = UpdateUserForm(instance=request.user)

	return render(request, 'registration/update_user.html', {'form': form})

