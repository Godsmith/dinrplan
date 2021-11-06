from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from .models import Day, Meal


def index(request):
    if request.user.is_authenticated:
        dates = [(date.today() + timedelta(days=i)) for i in range(7)]
        days = []
        for date_ in dates:
            try:
                day = Day.objects.get(date=date_)
            except Day.DoesNotExist:
                day = Day(date=date_, text="", user=request.user)
            days.append(day)
    else:
        days = []

    return render(request, "planner/index.html", {"days": days})


def showday(request, date_: str):
    try:
        day = Day.objects.get(date=date.fromisoformat(date_))
        text = day.text
    except Day.DoesNotExist:
        text = ""
    return render(request, "planner/day.html", {"date": date_, "text": text})


def editday(request, date_):
    text = request.POST["text"]
    try:
        day = Day.objects.get(date=date.fromisoformat(date_))
        day.text = text
        day.save()
    except Day.DoesNotExist:
        day = Day(date=date.fromisoformat(date_), text=text, user=request.user)
        day.save()

    return HttpResponseRedirect(reverse("index"))


class MealCreateView(CreateView):
    model = Meal
    template_name = "planner/createmeal.html"
    fields = ["name", "source", "persons", "time", "ingredients", "steps"]
    success_url = "/"  # reverse("index")  # this does not work for some reason

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial["name"] = self.kwargs["text"]
    #     return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
