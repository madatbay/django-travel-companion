from django.contrib import admin
from .models import Destination, Trip, Budget, BudgetItem


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


class BudgetItemInline(admin.TabularInline):
    model = BudgetItem


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    inlines = [BudgetItemInline]
    list_display = ["name", "trip"]
    search_fields = ["name", "trip", "created_at"]
    list_filter = ["created_at"]
    readonly_fields = ["created_at"]

    fieldsets = (
        (
            "General Information",
            {
                "fields": ("name", "trip", "created_at"),
            },
        ),
    )


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "img_preview", "created_at"]
    search_fields = ["name", "user", "created_at"]
    list_filter = ["created_at", "user"]
    readonly_fields = ["created_at"]

    fieldsets = (
        (
            "General Information",
            {
                "fields": ("name", "description", "user", "image", "created_at"),
            },
        ),
    )
