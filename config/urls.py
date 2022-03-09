from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic.base import TemplateView
from puppies.views import LitterList, AjaxLikeView, LikeView, UnlikeView, LitterRequestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), # new
    path('accounts/', include('django.contrib.auth.urls')),
    path('', LitterList.as_view(), name='home'),
    path('like/<int:pk>', LikeView, name='like_litter'),
    path(r'^ajaxlike/$', AjaxLikeView, name='ajaxlike'),
    path('unlike/<int:pk>', UnlikeView, name='unlike_litter'),
    path('shop/<int:pk>', LitterRequestView, name='shop_litter'),
]
