"""
    Script com funcoes para compilar e testar o programa enviado pelo SuSana
"""
import os
import subprocess
import re
from django.conf import settings

# PATHs usados no SuSana
SUSANA_FILES = "%s/susana-files/" % settings.BASE_DIR

# cria o diretorio de um novo usuario
def new_user(session_id, disciplina, lab):
    # seta o path
    path = SUSANA_FILES + disciplina + "/" + lab + "/"

    # cria o diretorio
    os.system("cd %s && mkdir %s" %(path, session_id))

# Compila o programa e retorna caso ocorra algum erro ou warning
def compilar(arquivos, disciplina, lab, username):
    # seta o path
    path = SUSANA_FILES + disciplina + "/" + lab + "/" + username + "/"

    filtro = re.compile(r'(;\s|\b)(system|exec(.|..|))\(')

    # verifica os arquivos fonte
    for arq in arquivos:
        # abre o arquivo
        arquivo = open(path + arq, 'r')
        fonte = arquivo.read()
        arquivo.close()

        # verifica se tem um comando do sistema
        if filtro.search(fonte) is not None:
            return u"error: Você não tem permissão para executar um comando do sistema!"

    ret = subprocess.getoutput("cd %s && gcc -std=c99 -pedantic -Wall -lm %s -o %s" %(path, " ".join(arquivos), username + ".out"))

    return ret

# Executa o programa e compara o arquivo, retornando o resultado
def testar(disciplina, lab, username, num_teste):
    # seta os paths
    path = SUSANA_FILES + disciplina + "/" + lab + "/"
    path_testes = path + "testes/"
    path += username + "/"

    # executa e salva a saida.
    ret = os.system("cd %s && timeout 5 ./%s <%sarq%02d.in >%sarq%02d.out" %(path, username + ".out", path_testes, int(num_teste), path, int(num_teste)))

    # Timeout retorna 124
    if (ret == 124):
        return "Timeout!"
    # Segmentation fault retorna 139
    if (ret == 139):
        return "Segmentation fault!"

    # compara a saida
    diff = subprocess.getoutput("diff %sarq%02d.out %sarq%02d.res" %(path, int(num_teste), path_testes, int(num_teste)))

    return diff

# cria o diretorio da disciplina
def cria_disciplina(disciplina):
    # realiza o mkdir
    os.system("cd %s && mkdir %s" %(SUSANA_FILES, disciplina))

# cria o diretorio do lab dentro da disciplina correspondente
def cria_lab(disciplina, lab, url_testes, qtd_testes, ext_entrada, ext_saida):
    # realia o mkdir
    os.system("cd %s && mkdir %s" %(SUSANA_FILES + disciplina + "/", lab))

    # define o path lab
    path_lab = SUSANA_FILES + disciplina + "/" + lab + "/"

    # cria os diretorios testes e out
    os.system("cd %s && mkdir %s" %(path_lab, "testes"))

    # define o path testes
    path_testes = path_lab + "testes/"

    # coloca barra no fim da url teste caso não exista
    if url_testes[-1] != '/':
        url_testes += '/'

    # realiza o download dos arquivos de teste
    for i in range(1, qtd_testes+1):
        os.system("cd %s && curl -k %sarq%02d.%s > arq%02d.in" %(path_testes, url_testes, i, ext_entrada, i)) # entrada
        os.system("cd %s && curl -k %sarq%02d.%s > arq%02d.res" %(path_testes, url_testes, i, ext_saida, i)) # saida

# apaga os diretórios e arquivos do lab
def apaga_lab(disciplina, lab):
    # apaga os diretórios e subdiretórios
    os.system("cd %s && rm -rf %s" % (SUSANA_FILES + disciplina, lab))

# apaga a disciplina e todos os subdiretórios
def apaga_disciplina(disciplina):
    os.system('cd %s && rm -rf %s' % (SUSANA_FILES, disciplina))