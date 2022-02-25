from django import forms

from .models import BudgetItem, Destination, Hotel, Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ("user", "trip_mates")


class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        exclude = ("budget",)


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        exclude = ("user",)


class TripDestinationForm(forms.ModelForm):
    """
    Form to add user destinations to the trip
    """
    destinations = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)

    def __init__(self, user, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        if user:
            self.fields["destinations"].queryset = Destination.objects.all().filter(user=user)

    class Meta:
        model = Trip
        fields = ("destinations",)


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        exclude = ("city",)