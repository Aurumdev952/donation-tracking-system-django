from django.db import models


# Create your models here.
class Cause(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tagline = models.CharField(max_length=150)
    description = models.TextField()
    end_date = models.DateTimeField()
    banner_image = models.ImageField(upload_to="images/")
    cover_image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name
