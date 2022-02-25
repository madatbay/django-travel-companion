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
    def is_completed(self):
        return date.today() > self.end_date


class Budget(models.Model):
    trip = models.OneToOneField("travel.Trip", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def get_total(self):
        items = self.budgetitem_set.all()
        total = 0
        for item in items:
            total += item.quantity * item.item_price
        return total


class BudgetItem(models.Model):
    budget = models.ForeignKey("travel.Budget", on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    item_price = models.PositiveIntegerField(default=0, help_text="Price for item per 1 quantity")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.label

    @property
    def get_subtotal(self):
        return self.quantity * self.item_price


class Destination(models.Model):
    user = models.ForeignKey("user.User", related_name="destination", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    descriptions = models.TextField(help_text="Short description for destination")
    image = models.ImageField(upload_to='destinations/', help_text="Image to identify destination easily")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    @property
    def img_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
        return "Not set"
