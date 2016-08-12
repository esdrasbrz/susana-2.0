from django.conf.urls import url
from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^check/$', views.check_login, name='check'),
    url(r'^out/$', views.logout_view, name='logout'),

    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^cadastro/salvar/$', views.salvar_usuario, name='salvar_usuario'),

    url(r'^alterar/$', views.alterar_login, name='alterar_login'),
    url(r'^alterar/salvar/$', views.salvar_login, name='salvar_login'),
]