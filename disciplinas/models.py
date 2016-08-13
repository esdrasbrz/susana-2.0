from django.db import models

"""
Tabela de disciplinas
"""
class Disciplinas(models.Model):
    codigo = models.CharField(max_length=5)
    turma = models.CharField(max_length=10)

    descricao = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['codigo']
        unique_together = (('codigo', 'turma'),)

    def __str__(self):
        return '%s%s' %(self.codigo, self.turma)