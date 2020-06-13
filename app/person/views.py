from django.shortcuts import render
from .models import Person

# Create your views here.
def person_view(request, person_id):
    obj = Person.objects.get(pk=person_id)
    context = {
        "object": obj
    }
    return render(request, "person/person.html", context)