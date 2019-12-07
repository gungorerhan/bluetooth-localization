from django.contrib import admin

from .models import Person, Card

# Register your models here.
admin.site.register(Person)
admin.site.register(Card)