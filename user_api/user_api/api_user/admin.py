from django.contrib import admin
from .import models

admin.site.register(models.Service)
admin.site.register(models.RequestService)
admin.site.register(models.Comment)