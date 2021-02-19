from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('customers/<str:pk>/',views.customers, name='customers'),
    path('products/', views.products, name='products'),
    path('ordered_order/', views.createOrder, name='ordered_form'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
]