from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from .models import Day, Meal


def index(request):
    week_deltas = [-1, 0]
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

    return render(request, "planner/index.html", {"weeks": weeks})


def showday(request, date_: str):
    day, _ = Day.objects.get_or_create(date=date.fromisoformat(date_))
    return render(request, "planner/day.html", {"day": day})


def editday(request, date_):
    text = request.POST["text"]
    meals = []
    for meal_name in text.split(Day.MEAL_NAME_DELIMITER):
        meal_name = meal_name.strip()
        # Raises MultipleObjectsReturned if the user has managed to create multiple meals in some way
        meal, _ = Meal.objects.get_or_create(author=request.user, name=meal_name)
        meals.append(meal)
    day, _ = Day.objects.get_or_create(
        date=date.fromisoformat(date_), user=request.user
    )
    day.meals.set(meals)

    return HttpResponseRedirect(reverse("index"))


class MealCreateView(CreateView):
    model = Meal
    template_name = "planner/createmeal.html"
    fields = ["name", "source", "persons", "time", "ingredients", "steps"]
    success_url = "/"  # reverse("index")  # this does not work for some reason

    def get_initial(self):
        """Prepoulate the name field with the meal name from the URL, e.g. createmeal/Pannkakor"""
        initial = super().get_initial()
        initial["name"] = self.kwargs["meal_name"]
        return initial

    def form_valid(self, form):
        """Add author to the created Meal object, since it is a mandatory field"""
        form.instance.author = self.request.user
        return super().form_valid(form)
