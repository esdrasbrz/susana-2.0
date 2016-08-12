from django.conf.urls import url
from . import views

app_name = 'labs'
urlpatterns = [
    url(r'^(?P<disciplina_id>[0-9]+)/$', views.seleciona_disciplina, name='seleciona_disciplina'),
    url(r'^seleciona_lab/(?P<lab_id>[0-9]+)/$', views.seleciona_lab, name='seleciona_lab'),
]