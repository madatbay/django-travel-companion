from datetime import date

from django.db import models
from django.utils.html import mark_safe


class Trip(models.Model):
    user = models.ForeignKey("user.User", related_name="trip", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, help_text="Short trip description")
    trip_mates = models.ManyToManyField(
        "user.User", related_name="mates", help_text="Choose who is going with you", blank=True
    )
    destinations = models.ManyToManyField(
        "travel.Destination", related_name="destinations", help_text="Add destinations to your trip", blank=True
    )
    start_date = models.DateField(help_text="Trip start date")
    end_date = models.DateField(help_text="Trip end date")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Trip: {self.name}x{self.pk}>"

    @property
    def is_completed(self) -> bool:
        return date.today() > self.end_date


class Budget(models.Model):
    trip = models.OneToOneField("travel.Trip", on_delete=models.CASCADE, help_text="Link Budget item to any trip")
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def get_total(self) -> float:
        total = 0
        for item in self.budgetitem_set.all():
            total += item.quantity * item.item_price
        return total


class BudgetItem(models.Model):
    budget = models.ForeignKey("travel.Budget", on_delete=models.CASCADE, help_text="Parent budget")
    label = models.CharField(max_length=50, help_text="Name for the expence")
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.FloatField(default=0, help_text="Price for item per 1 quantity")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> float:
        return self.label

    @property
    def get_subtotal(self) -> int:
        return self.quantity * self.item_price


class Destination(models.Model):
    user = models.ForeignKey("user.User", related_name="destination", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text="Destination name (City, Country, etc.)")
    description = models.TextField(help_text="Short description for destination")
    image = models.ImageField(upload_to="destinations/", help_text="Image to identify destination easily")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def img_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
        return "Not set"


class Hotel(models.Model):
    rate_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=200, help_text="Hotel address to locate it easily")
    city = models.ForeignKey("travel.Destination", on_delete=models.CASCADE, related_name="cities")
    rate = models.IntegerField(choices=rate_choices, default=1, help_text="Hotel rate you will stay")
    checkin_date = models.DateField(help_text="Date when is required to check in")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"<Hotel - {self.name}>"

    def __repr__(self) -> str:
        return f"<Hotel - {self.name}>"


class Flight(models.Model):
    user = models.ForeignKey("user.User", related_name="user", on_delete=models.CASCADE)
    trip = models.ForeignKey("travel.Trip", related_name="trip", on_delete=models.CASCADE)
    from_loc = models.ForeignKey("travel.Destination", related_name="from_loc", on_delete=models.CASCADE, help_text="Point the location where you will fly")
    to_loc = models.ForeignKey("travel.Destination", related_name="to_loc", on_delete=models.CASCADE, help_text="Point the destination where to fly")
    checkin_date = models.DateTimeField(help_text="Date when is required to check in")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def flight_name(self):
        return f"Flight {self.from_loc}-{self.to_loc}"

    def __str__(self) -> str:
        return f"Flight {self.from_loc}-{self.to_loc}"

    def __repr__(self) -> str:
        return f"<Flight {self.from_loc}-{self.to_loc}>"