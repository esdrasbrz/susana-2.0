from django.conf.urls import url
from . import views

app_name = 'labs'
urlpatterns = [
    url(r'^(?P<disciplina_id>[0-9]+)/$', views.seleciona_disciplina, name='seleciona_disciplina'),
]