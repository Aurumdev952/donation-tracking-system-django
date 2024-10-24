from django.urls import path

from . import views

urlpatterns = [
    path("config/", views.stripe_config),
    path("create-checkout-session/<int:pk>/", views.create_checkout_session),
    path("payment/success/", views.SuccessView.as_view()),
    path("payment/cancelled/", views.CancelledView.as_view()),
    path("payment/webhook/", views.stripe_webhook),
]
