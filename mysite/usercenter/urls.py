from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.register, name='register'),
        url(r'^avatar/$', views.upload_avatar, name='upload_avatar'),
        url(r'^activate/(?P<code>\w+)$', views.activate, name='user_activate'),
]
