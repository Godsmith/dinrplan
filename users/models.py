from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_week_offset = models.SmallIntegerField(default=0)
    number_of_weeks_to_show = models.PositiveSmallIntegerField(default=2)
