# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-08 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0005_auto_20160817_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='labs',
            name='argumentos',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
