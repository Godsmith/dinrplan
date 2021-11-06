from django.conf import settings
from django.db import models


class Day(models.Model):
    date = models.DateField()
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Meal(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
