from django.urls import path

from . import views

app_name = "user"

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
]
