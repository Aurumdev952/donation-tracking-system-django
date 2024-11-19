from datetime import date, timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Avg, F, Sum
from django.http import JsonResponse
from django.shortcuts import render

from cause.models import Cause
from donation.models import Donation


def is_admin(user: User):
    return user.profile.role == "Admin"

@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    total_causes = Cause.objects.count()
    total_donations = Donation.objects.aggregate(Sum("amount"))["amount__sum"] or 0
    avg_donation_per_cause = Donation.objects.aggregate(avg=Avg("amount"))["avg"] or 0
    total_donors = Donation.objects.values("donor").distinct().count()
    yesterday = date.today() - timedelta(days=1)
    today_donors = (
        Donation.objects.filter(created_at__date=date.today())
        .values("donor")
        .distinct()
        .count()
    )
    yesterday_donors = (
        Donation.objects.filter(created_at__date=yesterday)
        .values("donor")
        .distinct()
        .count()
    )
    donor_increase = (
        ((today_donors - yesterday_donors) / yesterday_donors) * 100
        if yesterday_donors > 0
        else 0
    )
    context = {
        "total_causes": total_causes,
        "total_donations": total_donations,
        "avg_donation_per_cause": avg_donation_per_cause,
        "total_donors": total_donors,
        "donor_increase": round(donor_increase, 2),
    }
    return render(request, "dashboard.html", context)


@login_required
@user_passes_test(is_admin)
def dashboard_data_view(request):
    donations_by_date = (
        Donation.objects.annotate(date=F("created_at__date"))
        .values("date")
        .annotate(total=Sum("amount"))
        .order_by("date")
    )
    donation_dates = [entry["date"] for entry in donations_by_date]
    total_donations_over_time = [entry["total"] for entry in donations_by_date]
    donations_per_cause = Cause.objects.annotate(
        total_donations=Sum("donation__amount")
    ).values("name", "total_donations")
    cause_names = [entry["name"] for entry in donations_per_cause]
    donations_per_cause = [
        entry["total_donations"] or 0 for entry in donations_per_cause
    ]
    return JsonResponse(
        {
            "donation_dates": donation_dates,
            "total_donations_over_time": total_donations_over_time,
            "cause_names": cause_names,
            "donations_per_cause": donations_per_cause,
        }
    )
