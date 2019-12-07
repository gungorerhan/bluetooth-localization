from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from person.models import Person

# Create your models here.
class Location(models.Model):
    x                   = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(9)])
    y                   = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0), MaxValueValidator(9)])
    number_of_visitors  = models.IntegerField(blank=False, null=False, default=0)

class Log(models.Model):
    x                   = models.DecimalField(blank=False, null=False, max_digits=3, decimal_places=2, 
                                            validators=[MinValueValidator(0.01), MaxValueValidator(9.99)])
    y                   = models.DecimalField(blank=False, null=False, max_digits=3, decimal_places=2, 
                                            validators=[MinValueValidator(0.01), MaxValueValidator(9.99)])
    time                = models.DateTimeField()
    person_id           = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.time = timezone.now()
        return super(Log, self).save(*args, **kwargs)

