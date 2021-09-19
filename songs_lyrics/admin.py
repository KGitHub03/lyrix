from django.contrib import admin
from django.db.models.fields import AutoField

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Song)