

from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate


from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Litter, LitterRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
import json


from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

class LitterList(LoginRequiredMixin, generic.ListView):
	login_url = 'accounts/login/'
	redirect_field_name = 'redirect_to'
	queryset = Litter.objects.filter(is_live=True).order_by('birth_date')
	template_name = 'puppylist.html'

@login_required
def AjaxLikeView(request):
	data={}

	if request.method == 'POST':
		user = request.user
		litter_id = request.POST.get('litter_id')
		like_tracker = []	
		
		litter 	    = get_object_or_404(Litter, id=litter_id)
		litter_name = "{}'s Litter!".format(litter.mother_name)

		was_liked =  litter.likes.filter(id=user.id).exists()
		
		LitterRequest.objects.filter(user=user).delete()

		if not was_liked: 
			LitterRequest.objects.create(user=user, litter=litter)
			
		for l in Litter.objects.all():

			if l.is_live:
				user_likes  = l.likes.all()
				liked_count = user_likes.count() if user_likes.count() != 0 else 1

				like_tracker += [{
					"id": l.id,
					"is_selected": "True" if str(l.id) == str(litter_id) else "False",
					"is_liked"   : "True" if str(l.id) == str(litter_id) and not was_liked else "False",
					"liked_count": user_likes.count(),
					"perc_male"  : "{}%".format(round(user_likes.filter(puppy_gender__in=["male"]).count()   / liked_count * 100, 2)),
					"perc_female": "{}%".format(round(user_likes.filter(puppy_gender__in=["female"]).count() / liked_count * 100, 2)),
					"perc_either": "{}%".format(round(user_likes.filter(puppy_gender__in=["either"]).count() / liked_count * 100, 2))
				}]


		messages = []
		if not was_liked:
			messages += [{"level": "success", "message": "Thanks, {}. We've noted your interest in {}!".format(request.user.first_name, litter_name)}]

		data = {'success' : True
			  , 'likes'   : like_tracker
			  , "messages": messages}
	
	return HttpResponse(json.dumps(data), content_type='application/json')


def LikeView(request, pk):
	litter = get_object_or_404(Litter, id=request.POST.get('litter_id'))
	litter.likes.add(request.user)
	messages.success(request, "We took note of your interest in {}'s Litter!".format(litter.mother_name.title()))
	return HttpResponseRedirect(reverse('home'))

def LitterRequestView(request, pk):
	litter_request = get_object_or_404(LitterRequest, id=pk)
	litter_request.user.is_shopping=True
	litter_request.user.save(update_fields=["is_shopping"]) 
	return redirect(litter_request.litter.stripe_link)

def UnlikeView(request, pk):
	litter = get_object_or_404(Litter, id=request.POST.get('litter_id'))
	litter.likes.remove(request.user)
	return HttpResponseRedirect(reverse('home'))




