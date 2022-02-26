from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import datetime
from user.models import User

from .forms import BudgetItemForm, DestinationForm, FlightForm, HotelForm, TripDestinationForm, TripForm
from .models import Budget, BudgetItem, Destination, Flight, Hotel, Trip


def index(request):
    if request.user.is_authenticated:
        return render(
            request,
            "travel/dashboard.html",
            {
                "trips": Trip.objects.filter(user=request.user),
                "destinations": Destination.objects.filter(user=request.user),
                "flights": Flight.objects.filter(user=request.user, checkin_date__gt=datetime.today()),
            },
        )
    return render(request, "travel/home.html")


@login_required
def trip_all(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, "travel/trip_all.html", {"trips": trips})


@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect("travel:trip_mate_add", id=trip.id)
    else:
        form = TripForm()
    return render(request, "travel/trip_create.html", {"form": form})


@login_required
def trip_detail(request, id):

    return render(request, "travel/trip_detail.html", {"trip": get_object_or_404(Trip, id=id)})


@login_required
def trip_update(request, id: int):
    trip = get_object_or_404(Trip, id=id)
    if request.method == "POST":
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect("travel:trip_detail", id=id)
    else:
        form = TripForm(instance=trip)
    return render(request, "travel/trip_create.html", {"form": form})


@login_required
def budget_detail(request, id: int):
    return render(
        request,
        "travel/budget_detail.html",
        {"budget": get_object_or_404(Trip, id=id).budget, "form": BudgetItemForm()},
    )


@login_required
def budget_item_delete(request, id: int):
    """
    Delete budget items seperately
    """
    budget_item = BudgetItem.objects.filter(id=id).first()
    if budget_item:
        budget_item.delete()
        return JsonResponse({"status": "true", "message": f"Budget item {id} successfully deleted"}, status=204)
    return JsonResponse({"status": "false", "message": f"Cannot delete budget item {id}"}, status=400)


@login_required
def budget_item_add_or_update(request, id: int):
    """
    Create budget item or update if it exists
    """
    budget = get_object_or_404(Budget, id=id)
    if request.method == "POST":
        if item_id := request.POST.get("budget_id"):
            form = BudgetItemForm(request.POST, instance=BudgetItem.objects.get(id=item_id))
        else:
            form = BudgetItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.budget = budget
            item.save()
    return redirect("travel:budget_detail", id=budget.trip.id)


@login_required
def trip_mate_add(request, id: int):
    """
    Add trip mates to the trip
    """
    trip = get_object_or_404(Trip, id=id)
    if request.method == "POST":
        users: list = request.POST.get("users").split(",")
        trip.trip_mates.clear()
        for user in users:
            if len(user):
                trip.trip_mates.add(User.objects.filter(email=user).first().id)
        return redirect("travel:trip_detail", id=id)
    context = {"users": User.objects.exclude(email=request.user.email), "mates": trip.trip_mates.all(), "trip": trip}
    return render(request, "travel/add_tripmates.html", context)


@login_required
def destination_all(request):
    destinations = Destination.objects.filter(user=request.user)
    return render(request, "travel/destination_all.html", {"destinations": destinations})


@login_required
def destination_create(request):
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect("travel:index")
    else:
        form = DestinationForm()
    return render(request, "travel/destination_create.html", {"form": form})


@login_required
def destination_update(request, id: int):
    instance = get_object_or_404(Destination, id=id)
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("travel:index")
    else:
        form = DestinationForm(instance=instance)
        hform = HotelForm()
    return render(request, "travel/destination_update.html", {"form": form, "destination": instance, "hform": hform})


@login_required
def trip_destination_add(request, id):
    """
    Add previously created destination to the trip
    """
    trip = get_object_or_404(Trip, id=id)
    if request.method == "POST":
        form = TripDestinationForm(request.user, request.POST, instance=trip)
        if form.is_valid():
            form.save()
            return redirect("travel:trip_detail", id=id)
    else:
        form = TripDestinationForm(request.user, instance=trip)
    return render(request, "travel/trip_destination_add.html", {"form": form})


@login_required
def destination_hotel_delete(request, des_id: int, hotel_id: int):
    if request.method == "POST":
        hotel = get_object_or_404(Hotel, id=hotel_id)
        hotel.delete()
    return redirect("travel:destination_update", id=des_id)


@login_required
def destination_hotel_add_or_update(request, id: int):
    """
    Create hotel item or update if it exists
    """
    destination = get_object_or_404(Destination, id=id)
    if request.method == "POST":
        if item_id := request.POST.get("hotel_id"):
            form = HotelForm(request.POST, instance=Hotel.objects.get(id=item_id))
        else:
            form = HotelForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.city = destination
            item.save()
    return redirect("travel:destination_update", id=id)


@login_required
def flight_list(request, id: int):
    return render(
        request,
        "travel/flight_list.html",
        {"flights": Flight.objects.filter(user=request.user, trip__id=id), "form": FlightForm()},
    )


@login_required
def flight_add_or_update(request, id: int):
    """
    Create flight or update if it exists
    """
    trip = get_object_or_404(Trip, id=id)
    if request.method == "POST":
        if item_id := request.POST.get("flight_id"):
            form = FlightForm(request.POST, instance=Flight.objects.get(id=item_id))
        else:
            form = FlightForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            if not "user" in item.__dict__.keys():
                item.user = request.user
                item.trip = trip
            item.save()
    return redirect("travel:flight_list", id=trip.id)


@login_required
def flight_delete(request, id: int):
    """
    Delete flight items seperately
    """
    flight = Flight.objects.filter(id=id).first()
    if flight:
        flight.delete()
        return JsonResponse({"status": "true", "message": f"Flight {id} successfully deleted"}, status=204)
    return JsonResponse({"status": "false", "message": f"Cannot delete flight {id}"}, status=400)
