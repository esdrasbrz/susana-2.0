# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0004_auto_20160812_0059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='submissoes',
            options={'ordering': ['-data_submissao']},
        ),
        migrations.RemoveField(
            model_name='submissoes',
            name='detalhes',
        ),
        migrations.AddField(
            model_name='submissoes',
            name='output_compilacao',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='submissoes',
            name='output_testes',
            field=models.TextField(null=True),
        ),
    ]
