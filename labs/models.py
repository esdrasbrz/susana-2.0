from django.db import models
from disciplinas.models import Disciplinas
from django.contrib.auth.models import User

"""
Tabela de Labs
"""
class Labs(models.Model):
    # relacionamento com disciplinas
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE)

    nome = models.CharField(max_length=50, unique=True)
    qtd_testes = models.IntegerField()
    arg_exec = models.CharField(max_length=255, null=True)
    arg_diff = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nome

"""
Tabela de Submissões
"""
class Submissoes(models.Model):
    lab = models.ForeignKey(Labs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    data_submissao = models.DateTimeField(auto_now_add=True)
    qtd_testes_corretos = models.IntegerField()

    output_compilacao = models.TextField(null=True)
    output_testes = models.TextField(null=True)

    def get_linhas_compilacao(self):
        return self.output_compilacao.split('\n')
    def get_linhas_testes(self):
        return self.output_testes.split('\n')

    class Meta:
        ordering = ['-data_submissao']