import json
from datetime import date
from datetime import timedelta
from typing import List

from django.db.models import Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import UpdateView

from .forms import UploadFileForm
from .models import Category
from .models import Comment
from .models import Day
from .models import Meal

FIRST_WEEK_OFFSET_OPTIONS = [0, 2, 6, 12, 18, 24]
DEFAULT_FIRST_WEEK_OFFSET = 0
NUMBER_OF_WEEKS_TO_SHOW_OPTIONS = [1, 2, 3, 6]
DEFAULT_NUMBER_OF_WEEKS_TO_SHOW = 3


def _get_weeks_and_reset_editing_status(request):
    # When (re)loading the page, reset the editing status of all days so that
    # clicking the edit button opens the edit view for those days again.
    request.session["editing"] = []
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
    return weeks


def index(request):
    return render(
        request,
        "planner/index.html",
        {
            "weeks": _get_weeks_and_reset_editing_status(request),
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

        return HttpResponseRedirect(reverse("planner:weeks"))


class WeeksView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "planner/weeks.html",
            {"weeks": _get_weeks_and_reset_editing_status(request)},
        )


class MealUpdateView(UpdateView):
    model = Meal
    template_name = "planner/modals/edit_meal.html"
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
    success_url = "not used since we override form_valid, but if we don't have this Django throws an exception"

    def form_valid(self, form):
        # Add author to the created Meal object, since it is a mandatory field
        form.instance.author = self.request.user
        # Also set is_recipe to True to show it as blue color and get it to show up in the recipe list
        form.instance.is_recipe = True

        super().form_valid(form)
        # Return the weeks view to htmx, so that the text color updates
        return HttpResponseRedirect(reverse("planner:weeks"))


class MealDetailView(DetailView):
    model = Meal
    template_name = "planner/modals/show_meal.html"
    fields = ["name", "source", "persons", "time", "ingredients", "steps"]


class MealDeleteView(View):
    def post(self, request, *args, **kwargs):
        keys = [key for key in request.POST.keys() if key.startswith("delete")]
        meal_pks = [int(key.split("-")[-1]) for key in keys]
        for pk in meal_pks:
            Meal.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse("planner:recipes"))


class DragView(View):
    """Called when dragging from or dropping on a day, when you want to move a set of meals from one day to another."""

    def post(self, request, *args, **kwargs):
        """When dragging from a day, store that date in a variable.
        When dropping on a day, exchange the meals of the source day and the target day."""
        event_type = json.loads(request.headers["Triggering-Event"])["type"]
        if event_type == "dragstart":
            request.session["date_dragged_from"] = kwargs["date"]
            return HttpResponse(status=204)
        elif event_type == "drop":
            source_day, _ = Day.objects.get_or_create(
                date=date.fromisoformat(request.session["date_dragged_from"]),
                user=request.user,
            )
            target_day, _ = Day.objects.get_or_create(
                date=date.fromisoformat(kwargs["date"]), user=request.user
            )
            previous_source_day_meals = list(source_day.meals.all())
            source_day.meals.set(target_day.meals.all())
            target_day.meals.set(previous_source_day_meals)
            return HttpResponseRedirect(reverse("planner:weeks"))


class EditDayView(View):
    def get(self, request, *args, **kwargs):
        editing: list = request.session.get("editing", [])
        date_ = kwargs["date"]

        if date_ in editing:
            # If we already were changing this day, store that
            # we are not anymore and return the non-editing day template
            editing.remove(date_)
            request.session["editing"] = editing
            return HttpResponseRedirect(
                reverse("planner:show_day", kwargs={"date": date_})
            )

        # Store that we are currently changing this day
        editing.append(kwargs["date"])
        request.session["editing"] = editing

        day, _ = Day.objects.get_or_create(
            date=date.fromisoformat(date_), user=request.user
        )
        todays_meal_names = [meal.name for meal in day.meals.all()]
        database_meals = [
            meal
            for meal in Meal.objects.filter(author=request.user)
            .annotate(num_days=Count("day"))
            .order_by("-num_days")
            if meal.is_recipe
        ]
        return render(
            request,
            "planner/modals/edit_day.html",
            {
                "day": day,
                "todays_meal_names": todays_meal_names,
                "database_meals": database_meals,
            },
        )

    def post(self, request, *args, **kwargs):
        meal_names = request.POST.getlist("select")  # type: List[str]
        meals = []
        for meal_name in meal_names:
            # Raises MultipleObjectsReturned if the user has managed to create multiple meals in some way
            meal, _ = Meal.objects.get_or_create(author=request.user, name=meal_name)
            meals.append(meal)
        iso_date = date.fromisoformat(kwargs["date"])
        day, _ = Day.objects.get_or_create(date=iso_date, user=request.user)
        day.meals.set(meals)

        return redirect("planner:show_day", date=iso_date)


class ShowDayView(View):
    def get(self, request, *args, **kwargs):
        day, _ = Day.objects.get_or_create(
            date=date.fromisoformat(kwargs["date"]), user=request.user
        )
        return render(
            request,
            "planner/modals/show_day.html",
            {
                "day": day,
            },
        )


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
                is_recipe=True,
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
            if meal.is_recipe
        ]
        return render(
            request,
            "planner/recipes.html",
            {"meals": created_meals},
        )
