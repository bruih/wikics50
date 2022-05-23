from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newPage", views.newPage, name="newPage"),
    path("wiki/<str:entry>", views.entryPage, name="entry"),
    path("wiki/<str:entry>/edit", views.editPage, name="edit"),
    path("searchPage", views.searchPage, name="search"),
    path("randomPage", views.randomPage, name="randomPage"),
]
