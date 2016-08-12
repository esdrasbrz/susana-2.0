from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from login.user_tests import *
from .models import *

"""
Lista todas as disciplinas para possíveis alterações
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def disciplinas(request):
    # lista todas as disciplinas
    disciplinas = Disciplinas.objects.all()

    return render(request, 'disciplinas/disciplinas.html', {'disciplinas': disciplinas})

"""
Cria uma nova disciplina para inserção
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def nova_disciplina(request):
    # renderiza o diálogo de alterar disciplina
    return render(request, 'disciplinas/alterarDisciplina.html', {'nova_disciplina': True})