"""
    Script com funcoes para compilar e testar o programa enviado pelo SuSana
"""
import os
import subprocess
import re
from django.conf import settings

# PATHs usados no SuSana
SUSANA_FILES = "%s/susana-files/" % settings.BASE_DIR

def normaliza_espacos(dir):
    return dir.replace(' ', '\ ')

# Compila o programa e retorna caso ocorra algum erro ou warning
def compilar(arquivos, lab, username):
    # seta o path
    path = SUSANA_FILES + str(lab.disciplina) + "/" + str(lab) + "/" + username + "/"

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

    ret = subprocess.getoutput("cd %s && gcc -Wall -Werror -ansi -pedantic -lm %s -o %s" %(normaliza_espacos(path), " ".join(arquivos), username + ".out"))

    return ret

# Executa o programa e compara o arquivo, retornando o resultado
# Somente utiliza a variável fonte em caso de linguagem não compilada (python)
def testar(lab, username, num_teste, linguagem, fonte):
    # coloca no padrao linux de espacos
    username = normaliza_espacos(username)

    # seta os paths
    path = SUSANA_FILES + normaliza_espacos(str(lab.disciplina)) + "/" + \
           normaliza_espacos(str(lab)) + "/" + username + "/"

    # dicionário com os comandos de execução do programa
    executar = {
        'c': './%s' % (username + ".out"),
        'python': 'python3 %s' % fonte
    }

    # executa e salva a saida.
    ret = os.system("cd %s && timeout 2 %s %s" %(path, executar[linguagem], lab.arg_exec.replace('[NUM]', '%02d' % num_teste)))

    # Timeout retorna 124
    if (ret == 124):
        return "Timeout!"
    # Segmentation fault retorna 139
    if (ret == 139):
        return "Segmentation fault!"

    # compara a saida
    diff = subprocess.getoutput("cd %s && diff %s" %(path, lab.arg_diff.replace('[NUM]', '%02d' % num_teste)))

    return diff

# cria o diretorio da disciplina
def cria_disciplina(disciplina):
    # coloca no padrao linux de espacos
    disciplina = normaliza_espacos(disciplina)

    # realiza o mkdir
    os.system("cd %s && mkdir %s" %(SUSANA_FILES, disciplina))

# cria o diretorio do lab dentro da disciplina correspondente
def cria_lab(lab, url_testes, arquivos):
    # coloca no padrão linux de espaços

    # realiza o mkdir
    os.system("cd %s && mkdir %s" %(SUSANA_FILES + normaliza_espacos(str(lab.disciplina)) + "/", normaliza_espacos(str(lab))))

    # define o path lab
    path_lab = SUSANA_FILES + str(lab.disciplina) + "/" + str(lab) + "/"
    path_lab = normaliza_espacos(path_lab)

    # cria os diretorios testes e out
    os.system("cd %s && mkdir %s" %(path_lab, "testes"))

    # define o path testes
    path_testes = path_lab + "testes/"

    # coloca barra no fim da url teste caso não exista
    if url_testes[-1] != '/':
        url_testes += '/'

    # separa os arquivos em uma lista
    arquivos = arquivos.split(',')

    # realiza o download dos arquivos de teste
    for i in range(1, lab.qtd_testes + 1):
        # troca o [NUM] pelo i
        arq_subs = [arq.replace('[NUM]', '%02d' % i) for arq in arquivos]

        # baixa os arquivos
        for arq in arq_subs:
            os.system("cd %s && curl -k -O %s" %(path_testes, url_testes + arq))

# apaga os diretórios e arquivos do lab
def apaga_lab(disciplina, lab):
    disciplina = normaliza_espacos(disciplina)

    # apaga os diretórios e subdiretórios
    os.system("cd %s && rm -rf %s" % (SUSANA_FILES + disciplina, lab))

# apaga a disciplina e todos os subdiretórios
def apaga_disciplina(disciplina):
    disciplina = normaliza_espacos(disciplina)

    os.system('cd %s && rm -rf %s' % (SUSANA_FILES, disciplina))
