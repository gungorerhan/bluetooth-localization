from django.contrib import admin

from .models import Location, Log

# Register your models here.
admin.site.register(Location)
admin.site.register(Log)