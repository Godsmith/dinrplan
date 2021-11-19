from django.contrib import admin

# Register your models here.
from .models import Day
from .models import Meal
from .models import Category

admin.site.register(Day)
admin.site.register(Meal)
admin.site.register(Category)
