from django.urls import path
from . import views

app_name = "travel"

urlpatterns = [
    path("", views.index, name="index"),
    path("trips/create/", views.create_trip, name="create_trip"),
    path("trips/<int:id>/", views.trip_detail, name="trip_detail"),
    path("trips/<int:id>/add-tripmates/", views.add_trip_mates, name="add_trip_mates"),
]
