from django.shortcuts import render
from disciplinas.models import Disciplinas
from .models import *
from django.contrib.auth.decorators import login_required

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

    # renderiza para a tela de submissões
    return render(request, 'labs/submissoes.html', {'lab': lab, 'submissoes': lab.submissao_set.all()})