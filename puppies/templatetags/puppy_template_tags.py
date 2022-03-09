from django import template
from django.contrib.auth import get_user_model

register = template.Library()


@register.filter
def on_closed_list(user):
	return user.on_closed_list()

@register.filter
def get_closed_list(user):
	return user.get_closed_list()

@register.filter
def get_allergy_friendly(litter):
	return litter.get_allergy_friendly()

@register.filter
def get_perc_likes(litter):
	user_count = get_user_model().objects.filter().count()
	like_count = litter.likes.count()

	if user_count == 0:
		return "0%"

	return "{}%".format(round(like_count/user_count * 100, 2))

@register.filter
def get_perc_likes_male(litter):

	user_ids = [user.id for user in get_user_model().objects.filter(puppy_gender__in=["male"])]

	like_count = litter.likes.count()
	male_like_count = litter.likes.filter(id__in=user_ids).count()


	if like_count == 0:
		return "0%"

	return "{}%".format(round(male_like_count/like_count * 100, 2))

@register.filter
def get_perc_likes_female(litter):

	user_ids = [user.id for user in get_user_model().objects.filter(puppy_gender__in=["female"])]

	like_count = litter.likes.count()
	female_like_count = litter.likes.filter(id__in=user_ids).count()

	if like_count == 0:
		return "0%"

	return "{}%".format(round(female_like_count/like_count * 100, 2))

@register.filter
def get_perc_likes_either(litter):

	user_ids = [user.id for user in get_user_model().objects.filter(puppy_gender__in=["either"])]

	like_count = litter.likes.count()
	either_like_count = litter.likes.filter(id__in=user_ids).count()

	if like_count == 0:
		return "0%"

	return "{}%".format(round(either_like_count/like_count * 100, 2))


@register.filter
def get_total_likes(litter):
	return str(litter.likes.filter().count())

@register.filter
def get_litter_size(litter):
    return litter.get_size()

@register.filter
def has_user_liked(litter, user):
	if user in litter.likes.all():
		return True
	return False
