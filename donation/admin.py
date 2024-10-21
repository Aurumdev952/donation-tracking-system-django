from django.contrib import admin

# Register your models here.
from .models import Cause, Donation

admin.site.register(Cause)
admin.site.register(Donation)
