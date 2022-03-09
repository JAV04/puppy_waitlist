from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomerInvite, CustomUser

class UserAdmin(admin.ModelAdmin):
	list_display  = ('username', 'date_joined', 'email', 'city', 'state', 'last_name', 'on_list', 'puppy_gender', 'have_allergies', 'is_shopping', 'purchased_puppy', 'puppy_notes')
	list_filter   = ('desired_size', 'is_shopping', 'purchased_puppy', 'state')
	search_fields = ['last_name', 'state']
	exclude       = ['password',]
	readonly_fields = ('pin', "email", "password")

	def on_list(self, obj):
		return obj.likes.through.objects.filter(user=obj).count() 

class CustomerInviteAdmin(admin.ModelAdmin):
    list_display = ('email', 'pin')
    list_filter = ('email',)
    readonly_fields = ('pin', )
    search_fields = ['last_name']

  

admin.site.register(CustomerInvite, CustomerInviteAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)