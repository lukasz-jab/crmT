from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home),
    path('home/', views.home),
    path('customers/<str:pk>/',views.customers),
    path('products/', views.products)

]