from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("search/results", views.results, name="results"),
    path("newpage", views.newpage, name="newpage"),
    path("see-new-page", views.show_newpage, name='show_newpage'),
    path('<str:title>/edit',views.edit,name='edit'),
    path('save', views.save_edit, name='save-edit'),
    path('random', views.random, name='random'),
    path("<str:title>", views.entry, name="title")
]
