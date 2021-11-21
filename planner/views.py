import json
from datetime import date, timedelta
from typing import List

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView, DetailView, CreateView, FormView
from django.utils.dateparse import parse_date

from .forms import UploadFileForm
from .models import Day, Meal, Comment, Category

FIRST_WEEK_OFFSET_OPTIONS = [0, 2, 6, 12, 18, 24]
DEFAULT_FIRST_WEEK_OFFSET = 0
NUMBER_OF_WEEKS_TO_SHOW_OPTIONS = [1, 2, 3, 6]
DEFAULT_NUMBER_OF_WEEKS_TO_SHOW = 3


def index(request):
    first_week_offset = (
        request.user.first_week_offset
        if request.user.is_authenticated
        else DEFAULT_FIRST_WEEK_OFFSET
    )
    number_of_weeks_to_show = (
        request.user.number_of_weeks_to_show
        if request.user.is_authenticated
        else DEFAULT_NUMBER_OF_WEEKS_TO_SHOW
    )
    week_deltas = range(
        -first_week_offset, -first_week_offset + number_of_weeks_to_show
    )
    monday_current_week = date.today() - timedelta(days=date.today().weekday())
    weeks = []
    if request.user.is_authenticated:
        for week_delta in week_deltas:
            monday = monday_current_week + timedelta(days=week_delta * 7)
            dates = [(monday + timedelta(days=i)) for i in range(7)]
            days = []
            for date_ in dates:
                date_.isoweekday()
                day, _ = Day.objects.get_or_create(date=date_, user=request.user)
                days.append(day)
            weeks.append(days)

    return render(
        request,
        "planner/index.html",
        {
            "weeks": weeks,
            "first_week_offsets": FIRST_WEEK_OFFSET_OPTIONS,
            "numbers_of_weeks_to_show": NUMBER_OF_WEEKS_TO_SHOW_OPTIONS,
        },
    )


class UpdateDisplayedWeeksView(View):
    def post(self, request, *args, **kwargs):
        request.user.first_week_offset = request.POST.get("first-week-offset")
        request.user.number_of_weeks_to_show = request.POST.get(
            "number-of-weeks-to-show"
        )
        request.user.save()

        return HttpResponseRedirect(reverse("planner:index"))


class MealUpdateView(UpdateView):
    model = Meal
    template_name = "planner/updatemeal.html"
    fields = [
        "name",
        "source",
        "persons",
        "time",
        "ingredients",
        "steps",
        "categories",
        "rating",
    ]
    success_url = (
        "/"  # reverse("index")  # this does not work; must be in get_success_url
    )

    def form_valid(self, form):
        """Add author to the created Meal object, since it is a mandatory field"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class MealDetailView(DetailView):
    model = Meal
    template_name = "planner/meal_detail.html"
    fields = ["name", "source", "persons", "time", "ingredients", "steps"]


class DayView(View):
    def get(self, request, *args, **kwargs):
        day, _ = Day.objects.get_or_create(
            date=date.fromisoformat(kwargs["date"]), user=request.user
        )
        todays_meal_names = [meal.name for meal in day.meals.all()]
        database_meal_names = [
            meal.name
            for meal in Meal.objects.filter(author=request.user)
            if meal.is_created
        ]
        return render(
            request,
            "planner/day.html",
            {
                "day": day,
                "todays_meal_names": todays_meal_names,
                "database_meal_names": database_meal_names,
            },
        )

    def post(self, request, *args, **kwargs):
        meal_names = request.POST.getlist("select")  # type: List[str]
        meals = []
        for meal_name in meal_names:
            # Raises MultipleObjectsReturned if the user has managed to create multiple meals in some way
            meal, _ = Meal.objects.get_or_create(author=request.user, name=meal_name)
            meals.append(meal)
        day, _ = Day.objects.get_or_create(
            date=date.fromisoformat(kwargs["date"]), user=request.user
        )
        day.meals.set(meals)

        return HttpResponseRedirect(reverse("planner:index"))


class CommentCreateView(CreateView):
    model = Comment
    template_name = "planner/createcomment.html"
    fields = ["text"]

    def get_success_url(self):
        return reverse("planner:showmeal", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        """Add author to the created Meal object, since it is a mandatory field"""
        form.instance.author = self.request.user

        meal_pk = self.kwargs["pk"]
        meal = get_object_or_404(Meal, pk=meal_pk)
        form.instance.meal = meal

        return super().form_valid(form)


class UploadJsonView(FormView):
    template_name = "planner/upload_json.html"
    form_class = UploadFileForm
    # fields = ["meals", "days"]
    success_url = "/"

    def form_valid(self, form):
        self._upload_meals(self.request.FILES["meals"])
        self._upload_days(self.request.FILES["days"])
        return super().form_valid(form)

    def _upload_meals(self, meals_file):
        bytes = meals_file.read()
        text = bytes.decode("utf-8")
        meal_dicts = json.loads(text)

        for meal_dict in meal_dicts:
            name = meal_dict["name"]
            source = meal_dict["source"]
            persons = meal_dict.get("servings", "") or "4"
            rating = meal_dict.get("rating", "") or "0"
            time = meal_dict["time"]
            ingredients = meal_dict["ingredients"]
            steps = meal_dict["steps"]
            category_names = meal_dict.get("categories", "").split(",")

            categories = []
            if category_names and category_names[0]:
                for category_name in category_names:
                    category, _ = Category.objects.get_or_create(name=category_name)
                    categories.append(category)

            comment_texts = meal_dict.get("comments", [])

            # Overwrite if there is an existing meal with the name
            if Meal.objects.filter(name=name).exists():
                Meal.objects.get(name=name).delete()

            meal = Meal.objects.create(
                author=self.request.user,
                name=name,
                source=source,
                persons=persons,
                time=time,
                ingredients=ingredients,
                steps=steps,
                rating=rating,
            )

            for category in categories:
                meal.categories.add(category)

            for comment_text in comment_texts:
                Comment.objects.create(
                    author=self.request.user, meal=meal, text=comment_text
                )

    def _upload_days(self, days_file):
        bytes = days_file.read()
        text = bytes.decode("utf-8")
        day_dicts = json.loads(text)
        for day_dict in day_dicts:
            try:
                date_ = parse_date(day_dict["date"])
            except TypeError:
                continue
            if not date_:
                continue
            day, _ = Day.objects.get_or_create(date=date_, user=self.request.user)
            day.meals.clear()
            meal_names_string = day_dict["meal"]
            if meal_names_string:
                meal_names = meal_names_string.split(";")
                for meal_name in meal_names:
                    meal, _ = Meal.objects.get_or_create(
                        name=meal_name, author=self.request.user
                    )
                    day.meals.add(meal)


class RecipesView(View):
    def get(self, request, *args, **kwargs):
        created_meals = [
            meal
            for meal in Meal.objects.filter(author=request.user).order_by("name")
            if meal.is_created
        ]
        return render(
            request,
            "planner/recipes.html",
            {"meals": created_meals},
        )
