from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.service_list_view, name='service_list'),
    path('services/<int:service_id>/', views.service_detail_view, name='service_detail'),
    path('book/<int:service_id>/', views.booking_view, name='booking'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'), 
    path('payment/success/<int:booking_id>/', views.payment_success, name='payment_success'), 
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('order_summary/<int:booking_id>/', views.order_summary_view, name='order_summary'),
    path('search/', views.search_view, name='search'),
]
