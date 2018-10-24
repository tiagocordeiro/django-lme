from django.db import models


class TimeSerie(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    code = models.CharField(max_length=50, blank=False, null=False)
