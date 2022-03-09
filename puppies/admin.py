from django.contrib import admin

from .models import Litter, LitterRequest, LitterArchive

from django.contrib.auth import get_user_model
from django.db.models import Case, Value, When


def toggle_live(modeladmin, request, queryset):
	queryset.update(is_live=Case(
		When(is_live=True, then=Value(False)),
		When(is_live=False, then=Value(True)),
	))
toggle_live.short_description = "Toggle visibility to user"

def archive_litter(modeladmin, request, queryset):
	for litter in queryset:
		if not litter.is_live:
			user_list = ""

			purchased_count, total_count = 0, 0
			for user in litter.likes.all():
				total_count += 1
				if user.purchased_puppy:
					user_list += "|| {} - {} - {} - {} - {} - {} ||\n".format(user.last_name, user.email, user.phonenumber, user.city, user.state, user.pickup_option)
					purchased_count += 1

			if (total_count == purchased_count) and (total_count > 0):
				LitterArchive.objects.create(mother_name=litter.mother_name, birth_date=litter.birth_date, user_list=user_list)
				for user in litter.likes.all():
					if user.purchased_puppy:
						get_user_model().objects.filter(id=user.id).delete()

				Litter.objects.filter(id=litter.id).delete()

archive_litter.short_description = "Archive purchased litter"

def give_purchase_pin(modeladmin, request, queryset):
    for litter_request in queryset:
    	if litter_request.litter.stripe_link_pin != "" and litter_request.litter.stripe_link != "":
	    	litter_request.email_shopping_request()
	    	litter_request.user.has_shopping_link = True
	    	litter_request.user.save(update_fields=["has_shopping_link"]) 
give_purchase_pin.short_description = "Send litter's purchase pin/link to the user"

def purchased_puppy(modeladmin, request, queryset):
	for litter_request in queryset:
		if not litter_request.user.purchased_puppy:
			litter_request.user.purchased_puppy = True
			litter_request.user.save(update_fields=["purchased_puppy"])

purchased_puppy.short_description = "Customer purchased this litter"

class LitterRequestAdmin(admin.ModelAdmin):
	list_display = ("litter", "user_join_date", "last_name", "puppy_gender", "email", "user_state", "pickup", "can_shop", "is_shopping", "purchased_puppy")
	list_filter = ("litter__mother_name", 'user__is_shopping', 'user__purchased_puppy',  'user__state')
	search_fields = ['litter__mother_name', 'user__last_name', "user__email" ]
	actions = [give_purchase_pin, purchased_puppy]
	ordering= ('litter__birth_date', 'user__date_joined', )

	def user_join_date(self, obj):
		return obj.user.date_joined

	def last_name(self, obj):
		return obj.user.last_name

	def puppy_gender(self, obj):
		return obj.user.puppy_gender

	def email(self, obj):
		return obj.user.email

	def user_state(self, obj):
		return obj.user.state

	def pickup(self, obj):
		return obj.user.pickup_option

	def can_shop(self, obj):
		return obj.user.has_shopping_link

	def is_shopping(self, obj):
		return obj.user.is_shopping

	def purchased_puppy(self, obj):
		return obj.user.purchased_puppy

class LitterAdmin(admin.ModelAdmin):
    list_display = ("__str__", 'birth_date', 'available_count', 'male_count', 'female_count', 'size', 'allergy_friendly', 'is_live', 'created_at')
    list_filter = ('size', 'allergy_friendly', 'is_live')
    search_fields = ['mother_name']
    exclude = ['likes',]
    actions = [toggle_live, archive_litter]
    ordering= ('birth_date', )


class LitterArchiveAdmin(admin.ModelAdmin):
    list_display = ("mother_name", "birth_date", "user_list")
    list_filter = ("mother_name", "birth_date")
    search_fields = ['mother_name']
    ordering= ('birth_date', )

    #inlines = [UserLikesInline,]

admin.site.register(LitterRequest, LitterRequestAdmin)
admin.site.register(Litter, LitterAdmin)
admin.site.register(LitterArchive, LitterArchiveAdmin)



