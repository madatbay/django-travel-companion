import email
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from user.models import User

from .forms import TripForm
from .models import Trip


def index(request):
    if request.user.is_authenticated:
        context = {"trips": Trip.objects.filter(user=request.user)}
        return render(request, "travel/dashboard.html", context)
    return render(request, "travel/home.html")


@login_required
def create_trip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect("travel:add_trip_mates", id=trip.id)
    else:
        form = TripForm()
    return render(request, "travel/create_trip.html", {"form": form})


@login_required
def edit_trip(request, id):
    trip = Trip.objects.get(id=id)
    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect("travel:trip_detail", id=id)
    else:
        form = TripForm(instance=trip)
    return render(request, "travel/create_trip.html", {"form": form})


@login_required
def add_trip_mates(request, id):
    trip = Trip.objects.get(id=id)
    if request.method == "POST":
        users = request.POST.get("users").split(",")
        trip.trip_mates.clear()
        for user in users:
            if len(user):
                trip.trip_mates.add(User.objects.get(email=user).id)
        return redirect("travel:trip_detail", id=id)
    context = {"users": User.objects.exclude(email=request.user.email), "mates": trip.trip_mates.all()}
    return render(request, "travel/add_tripmates.html", context)


def trip_detail(request, id):
    return render(request, "travel/trip_detail.html", {"trip": Trip.objects.get(id=id)})
