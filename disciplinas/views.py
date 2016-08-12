from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib import messages
from login.user_tests import *
from .models import *
from utils.arquivos import *

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

"""
Salva a disciplina no BD e cria os arquivos
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
@transaction.atomic
def salvar_disciplina(request):
    # cria a disciplina com os dados do form
    disciplina = Disciplinas(codigo=request.POST['codigo'],
                             turma=request.POST['turma'],
                             descricao=request.POST['descricao'])

    # salva a disciplina no BD
    disciplina.save()

    # cria o diretório para a disciplina
    cria_disciplina(str(disciplina))

    # renderiza à listagem
    messages.success(request, 'Disciplina salva com sucesso!')
    return disciplinas(request)