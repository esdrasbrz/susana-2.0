"""
    Script com funcoes para compilar e testar o programa enviado pelo SuSana

    Obs.: Script funciona em python 2.7
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
def compilar(fileName, disciplina, lab, session_id):
    # seta o path
    path = SUSANA_FILES + disciplina + "/" + lab + "/"

    filtro = re.compile(r'(;\s|\b)(system|exec(.|..|))\(')

    # verifica os arquivos fonte
    for arq in fileName.split(' '):
        if arq != "":
            # abre o arquivo
            arquivo = open(arq, 'r')
            fonte = arquivo.read()
            arquivo.close()

            # verifica se tem um comando do sistema
            if filtro.search(fonte) is not None:
                return u"error: Você não tem permissão para executar um comando do sistema"

    ret = subprocess.getoutput("gcc -std=c99 -pedantic -Wall -lm %s -o %s" %(fileName, path+session_id+".out"))

    return ret

# Seta as permissoes para o executavel
def set_permissao(fileName, disciplina, lab):
    # seta o path
    path = SUSANA_FILES + disciplina + "/" + lab + "/"

    os.system("chmod a-x %s" %(path+fileName+".out"))
    os.system("chmod u+x %s" %(path+fileName+".out"))

# Executa o programa e compara o arquivo, retornando o resultado
def testar(fileName, disciplina, lab, num):
    # seta os paths
    path = SUSANA_FILES + disciplina + "/" + lab + "/"
    path_testes = path + "testes/"
    path_out = path + "out/"

    # executa e salva a saida. Se o retorno for maior que 100, ele da timeout
    ret = os.system("cd %s && timeout 5 ./%s <%sarq%02d.in >%sarq%02d" %(path, fileName+".out", path_testes, int(num), path_out + fileName, int(num)))

    # Timeout retorna 124
    if (ret == 124):
        return "Timeout!"
    # Segmentation fault retorna 139
    if (ret == 139):
        return "Segmentation fault!"

    # compara a saida
    diff = subprocess.getoutput("diff %sarq%02d %sarq%02d.res" %(path_out + fileName, int(num), path_testes, int(num)))

    # apagar o arquivo de saida
    os.system("cd %s && rm %sarq%02d" %(path_out, fileName, int(num)))

    return diff

# Apaga o executavel e o codigo fonte dos arquivos
def limpar(session_id, disciplina, lab):
    # seta o path
    path = SUSANA_FILES + disciplina + "/" + lab + "/"
    # apaga os arquivos
    os.system("cd %s && rm %s && rm -rf %s" %(path, session_id + ".out", session_id))

# cria o diretorio da disciplina
def cria_disciplina(disciplina):
    # realiza o mkdir
    os.system("cd %s && mkdir %s" %(SUSANA_FILES, disciplina))

# cria o diretorio do lab dentro da disciplina correspondente
def cria_lab(disciplina, lab, url_testes, qtd_testes):
    # realia o mkdir
    os.system("cd %s && mkdir %s" %(SUSANA_FILES + disciplina + "/", lab))

    # define o path lab
    path_lab = SUSANA_FILES + disciplina + "/" + lab + "/"

    # cria os diretorios testes e out
    os.system("cd %s && mkdir %s" %(path_lab, "testes"))

    # define o path testes
    path_testes = path_lab + "testes/"

    # realiza o download dos arquivos de teste
    for i in range(1, qtd_testes+1):
        os.system("cd %s && curl -O -k %sarq%02d.in" %(path_testes, url_testes, i)) # entrada
        os.system("cd %s && curl -O -k %sarq%02d.res" %(path_testes, url_testes, i)) # saida

# apaga os diretórios e arquivos do lab
def apaga_lab(disciplina, lab):
    # apaga os diretórios e subdiretórios
    os.system("cd %s && rm -rf %s" % (SUSANA_FILES + disciplina, lab))

# apaga a disciplina e todos os subdiretórios
def apaga_disciplina(disciplina):
    os.system('cd %s && rm -rf %s' % (SUSANA_FILES, disciplina))