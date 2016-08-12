from django.conf.urls import url
from . import views

app_name = 'disciplinas'
urlpatterns = [
    url(r'^$', views.disciplinas, name='disciplinas'),
    url(r'^novo/$', views.nova_disciplina, name='nova_disciplina'),
    url(r'^novo/salvar/$', views.salvar_disciplina, name='salvar_disciplina'),
    url(r'^seleciona/$', views.seleciona_disciplina, name='seleciona_disciplina'),
    url(r'^excluir/$', views.excluir_disciplina, name='excluir_disciplina'),
]