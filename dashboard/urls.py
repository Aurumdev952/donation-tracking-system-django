from django.urls import path

from .views import dashboard_data_view, dashboard_view

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("data/", dashboard_data_view, name="dashboard_data"),
]
