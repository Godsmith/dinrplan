from django.conf import settings
from django.db import models
from django.utils.formats import date_format


class Day(models.Model):
    date = models.DateField()
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def weekday_name(self) -> str:
        return date_format(self.date, "l")


class Meal(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    source = models.CharField(max_length=200, blank=True)
    persons = models.IntegerField(default=4)
    time = models.CharField(max_length=200, blank=True)
    ingredients = models.CharField(max_length=1000, blank=True)
    steps = models.CharField(max_length=10000, blank=True)
