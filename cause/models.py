from datetime import date

from django.db import models


# Create your models here.
class Cause(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tagline = models.CharField(max_length=150)
    description = models.TextField()
    end_date = models.DateTimeField()
    banner_image = models.ImageField(upload_to="images/", blank=True)
    cover_image = models.ImageField(upload_to="images/", blank=True)

    @property
    def is_expired(self):
        return date.today() > self.end_date

    def __str__(self):
        return self.name
