from django.http import HttpResponseRedirect
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("day/<date_>", views.showday, name="showday"),
    path("editday/<date_>", views.editday, name="editday"),
    path("meal/edit/<slug:pk>", views.MealUpdateView.as_view(), name="updatemeal"),
    path("meal/show/<slug:pk>", views.MealDetailView.as_view(), name="showmeal"),
]
