from re import search
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name="home"),
    path('about_us/', views.about_us, name="about_us"),
    path("listings/", views.listing_index, name="listings"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout", views.logout, name="logout"),
    path("contact/", views.contact, name="contact"),
]
