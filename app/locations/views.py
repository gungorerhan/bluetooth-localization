from django.shortcuts import render
from .models import Location, Log
from .forms import UserTraceForm

# Create your views here.
def livelocations_view(request):
    context = {
        
    }
    return render(request, "locations/livelocations.html", context)

def heatmap_view(request):
    context = {

    }
    return render(request, "locations/heatmap.html", context)

def usertraces_main_view(request):
    form = UserTraceForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data['person_id'])
        form.save()
    context = {
        'form': form
    }
    return render(request, "locations/usertraces_main.html", context)

def usertraces_view(request, person_id):
    obj = Log.objects.get(person_id_id=person_id)
    context = {
        "object": obj
    }
    return render(request, "locations/usertraces.html", context)