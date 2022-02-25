from django.forms import ModelForm
from .models import Trip, BudgetItem

class TripForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ("user", "trip_mates")

class BudgetItemForm(ModelForm):
    class Meta:
        model = BudgetItem
        exclude = ("budget",)
