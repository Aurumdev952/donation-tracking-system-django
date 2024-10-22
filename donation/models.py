from django.contrib.auth.models import User
from django.db import models

from cause.models import Cause


class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cause = models.ForeignKey(Cause, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor} - {self.amount}"
