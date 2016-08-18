from django.conf.urls import url
from . import views

app_name = 'labs'
urlpatterns = [
    url(r'^(?P<disciplina_id>[0-9]+)/$', views.seleciona_disciplina, name='seleciona_disciplina'),
    url(r'^seleciona_lab/(?P<lab_id>[0-9]+)/$', views.seleciona_lab, name='seleciona_lab'),
    url(r'^seleciona_submissao/(?P<submissao_id>[0-9]+)/$', views.seleciona_submissao, name='seleciona_submissao'),

    url(r'^$', views.labs, name='labs'),
    url(r'^novo/$', views.novo_lab, name='novo_lab'),
    url(r'^novo/salvar/$', views.salvar_lab, name='salvar_lab'),
    url(r'^seleciona/$', views.seleciona_lab_alterar, name='seleciona_lab_alterar'),
    url(r'^excluir/$', views.excluir_lab, name='excluir_lab'),

    url(r'^seleciona_lab/(?P<lab_id>[0-9]+)/novo/$', views.nova_submissao, name='nova_submissao'),
]