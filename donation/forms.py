from django import forms

from .models import Cause, Donation


class CauseForm(forms.ModelForm):
    class Meta:
        model = Cause
        fields = [
            "name",
            "description",
            "banner_image",
            "tagline",
            "end_date",
            "cover_image",
        ]
