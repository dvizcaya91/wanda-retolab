from django.db import models


# Create your models here.
class Transaction(models.Model):

    date = models.DateField()
    category = models.CharField(max_length=200, default=None, null=True)
    product = models.CharField(max_length=200, default=None, null=True)
    subsector = models.CharField(max_length=200, default=None, null=True)
    price = models.FloatField()
    location = models.CharField(max_length=200, default=None, null=True)

    user_id = models.CharField(max_length=200, default=None, null=True)
    user_gender = models.CharField(max_length=200, default=None, null=True)
    companion_type = models.CharField(max_length=200, default=None, null=True)
    companion_gender = models.CharField(max_length=200, default=None, null=True)
    sons_age = models.IntegerField(default=0, null=True)
    travel_reason = models.CharField(max_length=200, default=None, null=True)
    type_of_traveler = models.CharField(max_length=200, default=None, null=True)
    origin = models.CharField(max_length=200, default=None, null=True)

