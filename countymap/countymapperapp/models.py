from django.db import models

# Create your models here.
class County(models.Model):
    name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=3)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)

