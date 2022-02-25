from django.urls import path
from . import views

app_name = "travel"

urlpatterns = [
    path("", views.index, name="index"),
    path("trips/create/", views.create_trip, name="create_trip"),
    path("trips/<int:id>/", views.trip_detail, name="trip_detail"),
    path("trips/<int:id>/add-tripmates/", views.add_trip_mates, name="add_trip_mates"),
    path("trips/<int:id>/edit/", views.edit_trip, name="edit_trip"),
    path("trips/<int:id>/budget/", views.budget_detail, name="budget_detail"),
    path("budget/delete/<int:id>/", views.delete_budget_item, name="delete_budget_item"),
    path("budget/add/<int:id>/", views.add_or_update_budget_item, name="add_or_update_budget_item"),
    path("destinations/create/", views.create_destination, name="create_destination"),
    path("destinations/<int:id>/update/", views.update_destination, name="update_destination"),
]
