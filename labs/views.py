from django.shortcuts import render
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from login.user_tests import *
from django.db import transaction
from utils.arquivos import *
from django.conf import settings
import os

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
Redireciona para a página para realizar nova submissão
"""
@login_required(login_url='/login/')
def nova_submissao(request, lab_id):
    # busca o lab
    lab = Labs.objects.get(pk=lab_id)

    # renderiza para a tela de detalhes
    return render(request, 'labs/submeter.html', {"lab": lab})

"""
Submete os arquivos .c e .h
"""
@login_required(login_url='/login/')
@transaction.atomic
def submeter(request, lab_id):
    # busca o lab
    lab = Labs.objects.get(pk=lab_id)

    # path no qual os arquivos serão salvos
    path = "%s/susana-files/%s/%s/%s/" % (settings.BASE_DIR, str(lab.disciplina), str(lab), request.user.username)
    arquivos = [] # lista com os nomes dos arquivos upados

    # cria um diretório com o usuário
    os.system("mkdir %s" % (path))

    # percorre os arquivos para fazer o upload
    for file in request.FILES.getlist('arquivos'):
        # verifica se o arquivo termina em .c ou .h
        if file.name[-2:] == '.c' or file.name[-2:] == '.h':
            # salva o nome do arquivo se terminar em .c
            if file.name[-2:] == '.c': arquivos.append(file.name)

            # salva os arquivos no diretório desse usuário
            with open(path + file.name, 'w') as output:
                output.write(str(file.read(), 'UTF-8'))

    # compila os arquivos
    output_compilacao = compilar(arquivos, str(lab.disciplina), str(lab), request.user.username)

    # string com as linhas de saida dos testes
    output_testes = ""
    qtd_testes_corretos = 0 # contador de testes corretos
    # verifica se não houve erro de compilação para realizar os testes
    if output_compilacao.lower().count('error') == 0:
        # percorre todos os testes
        for i in range(lab.qtd_testes):
            saida = testar(str(lab.disciplina), str(lab), request.user.username, i + 1)

            # verifica se o teste foi ok
            if saida == '':
                output_testes += "%02d: OK!\n" % (i + 1)
                qtd_testes_corretos += 1
            else:
                # exibe as linhas separadamente
                output_testes += "%02d:\n%s\n" %(i + 1, saida)

    # deleta o diretório do usuário
    os.system("rm -r %s" % (path))

    # cria a submissão no BD
    submissao = Submissoes()
    submissao.lab_id = lab_id
    submissao.user_id = request.user.id
    submissao.qtd_testes_corretos = qtd_testes_corretos
    submissao.output_compilacao = output_compilacao
    submissao.output_testes = output_testes

    # salva no BD
    submissao.save()

    # redireciona para a listagem de submissões
    return seleciona_lab(request, lab_id)

"""
Lista todos os labs
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def labs(request):
    labs = Labs.objects.all()

    return render(request, 'labs/labs.html', {'admin': True, 'labs': labs})

"""
Cria um novo lab
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def novo_lab(request):
    return render(request, 'labs/alterarLab.html', {"novo_lab": True, 'disciplinas': Disciplinas.objects.all()})

"""
Salva o Lab e baixa os arquivos de teste
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
@transaction.atomic
def salvar_lab(request):
    # Cria o lab com base nos parâmetros
    lab = Labs(nome=request.POST['nome'],
               disciplina_id=request.POST['disciplina'],
               qtd_testes=request.POST['qtd_testes'])

    # salva no banco de dados
    lab.save()

    # procura pela disciplina no BD
    disciplina = lab.disciplina
    # seta url para baixar testes
    url_testes = request.POST['url_testes']

    # cria o lab e baixa os testes
    cria_lab(str(disciplina), str(lab), url_testes, int(lab.qtd_testes))

    # retorna para a listagem de labs
    messages.success(request, 'Lab salvo com sucesso!')
    return labs(request)

"""
Seleciona o lab para fazer alterações
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
def seleciona_lab_alterar(request):
    # recebe o id como parâmetro
    id = request.GET['id']

    # procura o lab
    lab = Labs.objects.get(pk=id)
    # lista as disciplinas
    disciplinas = Disciplinas.objects.all()

    # renderiza a página de alteração
    return render(request, 'labs/alterarLab.html', {"lab": lab, "disciplinas": disciplinas})

"""
Exclui um lab e seus arquivos
"""
@login_required(login_url='/login/')
@user_passes_test(is_superuser, login_url='/login/')
@transaction.atomic
def excluir_lab(request):
    # recebe o lab
    lab = Labs.objects.get(pk=request.POST['id'])

    # apaga os arquivos do lab
    apaga_lab(str(lab.disciplina), str(lab))
    # apaga do BD
    lab.delete()

    # retorna para listar os labs
    messages.success(request, 'Lab excluído com sucesso!')
    return labs(request)