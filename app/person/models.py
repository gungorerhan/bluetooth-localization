from django.db import models
from django.utils import timezone

# Create your models here.
class Card(models.Model):
    card_id         = models.CharField(max_length=100, primary_key=True)
    activation_time = models.DateTimeField()
    card_type       = models.CharField(max_length=1, blank=False, null=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.activation_time = timezone.now()
        return super(Card, self).save(*args, **kwargs)

class Person(models.Model):
    person_id       = models.CharField(max_length=100, primary_key=True)
    first_name      = models.CharField(max_length=100, blank=False, null=False)
    last_name       = models.CharField(max_length=100, blank=False, null=False)
    card_id         = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True)
    date_of_birth   = models.DateTimeField()