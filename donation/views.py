import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from cause.models import Cause

from .models import Donation


class SuccessView(TemplateView):
    template_name = "donation-success.html"


class CancelledView(TemplateView):
    template_name = "donation-cancel.html"


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, pk):
    if request.method == "GET":
        domain_url = "http://127.0.0.1:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url
                + "donation/payment/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "donation/payment/cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price": "price_1QDNjALZvTUR5WIHOFYuOVUs",
                        "quantity": 1,
                    }
                ],
                payment_intent_data={
                    "metadata": {
                        "id": pk,
                        "user_id": (
                            request.user.id if request.user.is_authenticated else None
                        ),
                    }
                },
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "charge.succeeded":
        data = event["data"]["object"]["metadata"]
        amount = event["data"]["object"]["amount"]
        cause = get_object_or_404(Cause, pk=data["id"])
        user = get_object_or_404(User, id=data["user_id"])
        Donation.objects.create(donor=user, amount=amount / 100, cause=cause).save()


    return HttpResponse(status=200)
