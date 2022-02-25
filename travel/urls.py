from django.urls import path

from . import views

app_name = "travel"

urlpatterns = [
    path("", views.index, name="index"),
    path("trips/all/", views.trip_all, name="trip_all"),
    path("trips/create/", views.trip_create, name="trip_create"),
    path("trips/<int:id>/", views.trip_detail, name="trip_detail"),
    path("trips/<int:id>/edit/", views.trip_update, name="trip_update"),
    path("trips/<int:id>/add-tripmates/", views.trip_mate_add, name="trip_mate_add"),
    path("trips/<int:id>/add-destination/", views.trip_destination_add, name="trip_destination_add"),
    path("trips/<int:id>/budget/", views.budget_detail, name="budget_detail"),
    path("budget/delete/<int:id>/", views.budget_item_delete, name="budget_item_delete"),
    path("budget/add/<int:id>/", views.budget_item_add_or_update, name="budget_item_add_or_update"),
    path("destinations/all/", views.destination_all, name="destination_all"),
    path("destinations/create/", views.destination_create, name="destination_create"),
    path("destinations/<int:id>/update/", views.destination_update, name="destination_update"),
    path("destinations/<int:des_id>/hotels/<int:hotel_id>/delete/", views.destination_hotel_delete, name="destination_hotel_delete"),
    path("destinations/<int:id>/hotels/add/", views.destination_hotel_add_or_update, name="destination_hotel_add_or_update"),

]
