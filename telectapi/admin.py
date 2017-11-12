from django.contrib import admin

from telectapi import models

admin.site.register(models.User)
admin.site.register(models.Collection)
admin.site.register(models.Source)
