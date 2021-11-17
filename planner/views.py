from datetime import date, timedelta
from typing import List

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView, DetailView, CreateView

from .models import Day, Meal, Comment


def index(request):
    week_deltas = [-3, -2, -1, 0]
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


class MealUpdateView(UpdateView):
    model = Meal
    template_name = "planner/updatemeal.html"
    fields = ["name", "source", "persons", "time", "ingredients", "steps"]
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
