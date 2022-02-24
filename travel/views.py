from django.shortcuts import render
from .models import Trip

def index(request):
    if request.user.is_authenticated:
        context = {
            "trips": Trip.objects.filter(user=request.user)
        }
        return render(request, 'travel/dashboard.html', context)
    return render(request, 'travel/home.html')
