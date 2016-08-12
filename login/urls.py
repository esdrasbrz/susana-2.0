from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check/$', views.check_login, name='check'),
    url(r'^out/$', views.logout_view, name='logout'),
]