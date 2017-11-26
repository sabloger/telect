import datetime

import jwt
from django.contrib.auth.models import User as dUser
from django.db import models
from django.utils import timezone
from django_mysql.models import JSONField


class User(models.Model):
    mobile = models.CharField(max_length=255)
    session_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.mobile

    def make_token(self):
        return jwt.encode({'user_id': (self.id * 2) + 5987456}, 'secret', algorithm='HS256')

    @staticmethod
    def from_token(token):
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return User.objects.get(id=(payload['user_id'] - 5987456) / 2)


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
    name = models.CharField(max_length=255, )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

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
    last_fm_time = models.DateTimeField(default=timezone.now, null=True)
    are_collecting = models.BooleanField(default=False)
    collection = models.ForeignKey(Collection, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.source_data['username']


class AuthTemp(models.Model):
    mobile = models.CharField(max_length=255)
    phone_code_hash = models.CharField(max_length=255)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone_code_hash
