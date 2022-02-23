from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import CustomUserChangeForm, CustomUserCreationForm


def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("travel:home")
    form = CustomUserCreationForm()
    return render(request, "user/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("travel:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, "user/login.html", {"form": form})


@login_required
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("travel:home")


@login_required
def profile(request):
    return render(request, "user/profile.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, "Profile successfully updated.")
            return redirect("user:profile")
    form = CustomUserChangeForm(instance=request.user)
    return render(request, "user/edit_profile.html", {"form": form})
