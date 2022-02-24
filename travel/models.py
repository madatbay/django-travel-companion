from datetime import date

from django.db import models


class Trip(models.Model):
    user = models.ForeignKey("user.User", related_name="user", on_delete=models.CASCADE)
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
