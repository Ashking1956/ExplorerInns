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
    path('add_listing/', views.add_listing, name='add_listing'),
    path('update_listing/<int:listing_id>/', views.update_listing, name='update_listing'),
    path('delete_listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('realtor/add/', views.add_realtor, name='add_realtor'),
    path('realtor/<int:pk>/update/', views.update_realtor, name='update_realtor'),
    path('realtor/<int:pk>/delete/', views.delete_realtor, name='delete_realtor'),
]
