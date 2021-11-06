from datetime import date, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Day


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
