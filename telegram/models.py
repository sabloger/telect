import datetime

from django.db import models
from django_mysql.models import JSONField


class User(models.Model):
    mobile = models.CharField(max_length=255)
    session_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.mobile


class Collection(models.Model):
    TELEGRAM = 'TG'
    TYPES = (
        (TELEGRAM, 'Telegram'),
    )
    destination_type = models.CharField(
        max_length=2,
        choices=TYPES,
        default=TELEGRAM,
    )
    destination_data = JSONField()
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name


class Source(models.Model):
    TELEGRAM = 'TG'
    TYPES = (
        (TELEGRAM, 'Telegram'),
    )
    type = models.CharField(
        max_length=2,
        choices=TYPES,
        default=TELEGRAM,
    )
    source_data = JSONField()
    last_fm_id = models.BigIntegerField(default=0, null=True)
    last_fm_time = models.DateTimeField(default=datetime.datetime.now, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.source_data['username']
