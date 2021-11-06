from datetime import date, timedelta
from django.shortcuts import render


def index(request):
    dates = [(date.today() + timedelta(days=i)).isoformat() for i in range(7)]
    return render(request, "planner/index.html", {"dates": dates})


def editday(request, date):
    return render(request, "planner/editday.html", {"date": date})
