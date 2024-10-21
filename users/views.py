from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data["phone"]:
                user.profile.phone = form.cleaned_data["phone"]
                user.profile.save()
            auth_login(request, user)
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})
