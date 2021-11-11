from django.contrib import admin

# Register your models here.
from .models import Day
from .models import Meal

admin.site.register(Day)
admin.site.register(Meal)
