from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from login.user_tests import *
from django.db import transaction

"""
Seleciona a disciplina e lista todos os Labs referentes a ela
"""
@login_required(login_url='/login/')
def seleciona_disciplina(request, disciplina_id):
    # recebe a disciplina
    disciplina = Disciplinas.objects.get(pk=disciplina_id)

    # rederiza listando todos os labs
    return render(request, 'labs/labs.html', {'labs': disciplina.labs_set.all(), 'disciplina': disciplina})

"""
Seleciona o Lab para fazer a submissão
"""
@login_required(login_url='/login/')
def seleciona_lab(request, lab_id):
    # procura o lab
    lab = Labs.objects.get(pk=lab_id)
    # procura as submissoes
    submissoes = lab.submissoes_set.filter(user_id=request.user.id).all()

    # renderiza para a tela de submissões
    return render(request, 'labs/submissoes.html', {'lab': lab, 'submissoes': submissoes})

"""
Seleciona a submissão para exibir os detalhes
"""
@login_required(login_url='/login/')
def seleciona_submissao(request, submissao_id):
    # busca a submissão
    submissao = Submissoes.objects.get(pk=submissao_id)

    # renderiza para a tela de detalhes
    return render(request, 'labs/detalhes_submissao.html', {"submissao": submissao})


"""
Lista todos os labs
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def labs(request):
    labs = Labs.objects.all()

    return render(request, 'labs/labs.html', {'admin': True})