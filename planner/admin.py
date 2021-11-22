from django.contrib import admin

from .models import Category
from .models import Day
from .models import Meal

# Register your models here.

admin.site.register(Day)
admin.site.register(Meal)
admin.site.register(Category)
