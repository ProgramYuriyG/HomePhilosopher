from django.db import models

# Create your models here.
class ParseBatch(models.Model):
    status = models.IntegerField()


class County(models.Model):
    name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=3)
    latitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)


class Offense(models.Model):
    run = models.ForeignKey(ParseBatch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    county_name = models.CharField(max_length=50)
    state_code = models.CharField(max_length=10)


class Precipitation(models.Model):
    run = models.ForeignKey(ParseBatch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=12, decimal_places=8)
    units = models.CharField(max_length=50)
    county_name = models.CharField(max_length=50)
    state_code = models.CharField(max_length=10)


class Pollutant(models.Model):
    run = models.ForeignKey(ParseBatch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=12, decimal_places=8)
    units = models.CharField(max_length=50)
    fips_code = models.CharField(max_length=10)
