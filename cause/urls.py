from django.urls import path

from .views import cause_create, cause_delete, cause_detail, cause_list, cause_update

urlpatterns = [
    path("", cause_list, name="cause_list"),
    path("<int:pk>/", cause_detail, name="cause_detail"),
    path("create/", cause_create, name="create_cause"),
    path("cause/<int:pk>/edit/", cause_update, name="cause_update"),
    path("cause/<int:pk>/delete/", cause_delete, name="cause_delete"),
]
