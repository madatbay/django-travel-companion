from django.forms import ModelForm
from .models import Trip

class TripForm(ModelForm):
    class Meta:
        model = Trip
        exclude = ["user", "trip_mates"]
