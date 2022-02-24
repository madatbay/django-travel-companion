from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "start_date", "end_date", "created_at"]
    list_filter = ["user", "start_date", "end_date", "created_at"]
    search_fields = ["name", "user", "start_date", "end_date", "created_at"]
    filter_horizontal = ["trip_mates"]

    fieldsets = (
        (
            "General Information",
            {
                "fields": ("user", "name", "description"),
            },
        ),
        (
            "Options",
            {
                "fields": ("trip_mates",),
            },
        ),
        (
            "Schedule",
            {
                "fields": ("start_date", "end_date"),
            },
        ),
    )
