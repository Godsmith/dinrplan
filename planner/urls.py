from django.http import HttpResponseRedirect
from django.urls import path

from . import views

app_name = "planner"
urlpatterns = [
    path("", views.index, name="index"),
    path("day/<date>", views.DayView.as_view(), name="day"),
    path("meal/edit/<slug:pk>", views.MealUpdateView.as_view(), name="editmeal"),
    path("meal/show/<slug:pk>", views.MealDetailView.as_view(), name="showmeal"),
    path(
        "meal/comment/<slug:pk>",
        views.CommentCreateView.as_view(),
        name="createcomment",
    ),
    path("upload", views.UploadJsonView.as_view(), name="upload"),
    path("update_weeks", views.UpdateDisplayedWeeksView.as_view(), name="update_weeks"),
    path("recipes", views.RecipesView.as_view(), name="recipes"),
    path("weeks", views.WeeksView.as_view(), name="weeks"),
]
