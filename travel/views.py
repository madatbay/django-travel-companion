import email
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from user.models import User

from .forms import BudgetItemForm, DestinationForm, TripForm
from .models import Budget, BudgetItem, Destination, Trip


def index(request):
    if request.user.is_authenticated:
        context = {
            "trips": Trip.objects.filter(user=request.user),
            "destinations": Destination.objects.filter(user=request.user),
        }
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
def budget_detail(request, id):
    context = {"budget": Budget.objects.get(trip=id), "form": BudgetItemForm()}
    return render(request, "travel/budget_detail.html", context)


@login_required
def delete_budget_item(request, id):
    budget_item = BudgetItem.objects.filter(id=id).first()
    if budget_item:
        budget_item.delete()
        return JsonResponse({"status": "true", "message": f"Budget item {id} successfully deleted"}, status=204)
    return JsonResponse({"status": "false", "message": f"Cannot delete budget item {id}"}, status=400)


@login_required
def add_or_update_budget_item(request, id):
    budget = Budget.objects.get(id=id)
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


@login_required
def trip_detail(request, id):
    return render(request, "travel/trip_detail.html", {"trip": Trip.objects.get(id=id)})


@login_required
def create_destination(request):
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect("travel:index")
    else:
        form = DestinationForm()
    return render(request, "travel/destination_form.html", {"form": form})


@login_required
def update_destination(request, id):
    instance = Destination.objects.get(id=id)
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("travel:index")
    else:
        form = DestinationForm(instance=instance)
    return render(request, "travel/destination_form.html", {"form": form})