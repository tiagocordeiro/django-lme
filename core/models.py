from django.db import models


class TimeSerie(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(unique=True, max_length=50, blank=False, null=False)


class Serie(models.Model):
    code = models.ForeignKey(TimeSerie, on_delete=models.CASCADE)
    date = models.DateField()
    cash = models.DecimalField(decimal_places=2, max_digits=20)

class LondonMetalExchange(models.Model):
    date = models.DateField(unique=True)
    cobre = models.DecimalField(decimal_places=2, max_digits=20)
    zinco = models.DecimalField(decimal_places=2, max_digits=20)
    aluminio = models.DecimalField(decimal_places=2, max_digits=20)
    chumbo = models.DecimalField(decimal_places=2, max_digits=20)
    estanho = models.DecimalField(decimal_places=2, max_digits=20)
    niquel = models.DecimalField(decimal_places=2, max_digits=20)
    dolar = models.DecimalField(decimal_places=2, max_digits=20)

