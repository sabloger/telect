# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 14:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telectapi', '0003_auto_20171113_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
    ]
