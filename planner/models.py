from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.formats import date_format


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Meal(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    source = models.CharField(max_length=200, blank=True)
    persons = models.PositiveSmallIntegerField(
        default=4, validators=[MinValueValidator(1)]
    )
    time = models.CharField(max_length=200, blank=True)
    ingredients = models.TextField(max_length=1000, blank=True)
    steps = models.TextField(max_length=10000, blank=True)
    rating = models.PositiveSmallIntegerField(
        default=0, validators=[MaxValueValidator(5)]
    )
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_created(self) -> bool:
        """A meal is considered created when it has ingredients"""
        return bool(self.ingredients or self.source)

    @property
    def categories_text(self) -> str:
        return ", ".join(category.name for category in self.categories.all())

    def __str__(self):
        return self.name


class Day(models.Model):
    MEAL_NAME_DELIMITER = ";"

    date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Meal)

    def __str__(self):
        return str(self.date)

    def weekday_name(self) -> str:
        return date_format(self.date, "l")

    def text(self) -> str:
        return self.MEAL_NAME_DELIMITER.join(meal.name for meal in self.meals.all())


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    text = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}: {self.text}"
