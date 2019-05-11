from django.db import models

class HistoryValue(models.Model):
    temperature = models.CharField(max_length=32)
    pressure = models.CharField(max_length=32)
    altitude = models.CharField(max_length=32)
    sealevelPressure = models.CharField(max_length=32)
    time = models.DateTimeField(auto_now=True)