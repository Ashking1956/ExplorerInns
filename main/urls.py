from re import search
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('home/', views.index, name="home"),
    path('about_us/', views.about_us, name="about_us"),
    path("listings/", views.listing_index, name="listings"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
]
