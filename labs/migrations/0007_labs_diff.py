# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-08 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0006_labs_argumentos'),
    ]

    operations = [
        migrations.AddField(
            model_name='labs',
            name='diff',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
