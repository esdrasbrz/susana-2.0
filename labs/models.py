from django.db import models
from disciplinas.models import Disciplinas


"""
Tabela de Labs
"""
class Labs(models.Model):
    # relacionamento com disciplinas
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE)

    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome