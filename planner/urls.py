from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("editday/<date>", views.editday, name="editday"),
]
