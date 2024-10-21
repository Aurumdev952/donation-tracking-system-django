from django.contrib.auth.models import User
from django.db import models


class Cause(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tagline = models.CharField(max_length=150)
    description = models.TextField()
    end_date = models.DateTimeField()
    banner_image = models.ImageField(upload_to="uploads/")
    cover_image = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return self.name


class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.full_name} - {self.amount}"
