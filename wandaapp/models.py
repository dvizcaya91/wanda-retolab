from django.db import models


# Create your models here.
class Transaction(models.Model):

    date = models.DateField()
    category = models.CharField(max_length=200, default='Naturaleza', null=True)
    product = models.CharField(max_length=200, default='NA', null=True)
    subsector = models.CharField(max_length=200, default='Agencia de Viajes', null=True)
    price = models.FloatField(default=100000)
    location = models.CharField(max_length=200, default='Barranquilla', null=True)

    user_id = models.CharField(max_length=200, default='1032444591', null=True)
    user_gender = models.CharField(max_length=200, default='H', null=True)
    companion_type = models.CharField(max_length=200, default='Familia', null=True)
    companion_gender = models.CharField(max_length=200, default='M', null=True)
    sons_age = models.IntegerField(default=2, null=True)
    travel_reason = models.CharField(max_length=200, default='Turismo', null=True)
    type_of_traveler = models.CharField(max_length=200, default='Nacional', null=True)
    origin = models.CharField(max_length=200, default='Bogota', null=True)

