from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CauseForm
from .models import Cause


def is_admin(user: User):
    return user.profile.role == "Admin"


# Create your views here.
@login_required
@user_passes_test(is_admin)
def cause_create(request):
    if request.method == "POST":
        form = CauseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/causes")
    else:
        form = CauseForm()
    return render(request, "create.html", {"form": form})


@login_required
def cause_list(request):
    causes = Cause.objects.annotate(total_donations=Sum("donation__amount"))
    return render(request, "index.html", {"causes": causes})


@login_required
@user_passes_test(is_admin)
def cause_delete(request, pk):
    cause = get_object_or_404(Cause, pk=pk)
    if request.method == "POST":
        cause.delete()
        return redirect("/causes")
    return render(request, "cause_confirm_delete.html", {"cause": cause})


@login_required
@user_passes_test(is_admin)
def cause_update(request, pk):
    cause = get_object_or_404(Cause, pk=pk)
    if request.method == "POST":
        form = CauseForm(request.POST, request.FILES, instance=cause)
        if form.is_valid():
            form.save()
            return redirect("/causes", pk=cause.pk)
    else:
        form = CauseForm(instance=cause)
    return render(request, "create.html", {"form": form})


def cause_detail(request, pk):
    cause = get_object_or_404(Cause, pk=pk)
    return render(request, "cause_detail.html", {"cause": cause})
