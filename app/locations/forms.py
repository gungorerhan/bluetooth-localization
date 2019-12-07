from django import forms
from .models import Location, Log
from person.models import Person, Card

class UserTraceForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = [
            'person_id',
        ]
        
 