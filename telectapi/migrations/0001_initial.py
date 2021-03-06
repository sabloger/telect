# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 10:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_type', models.CharField(choices=[('TG', 'Telegram')], default='TG', max_length=2)),
                ('destination_data', django_mysql.models.JSONField(default=dict)),
                ('name', models.CharField(max_length=255)),
                ('payed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('TG', 'Telegram')], default='TG', max_length=2)),
                ('source_data', django_mysql.models.JSONField(default=dict)),
                ('last_fm_id', models.BigIntegerField(default=0, null=True)),
                ('last_fm_time', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='telectapi.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=255)),
                ('session_name', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telectapi.User'),
        ),
    ]
