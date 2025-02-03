from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name='home'),
    path('services/', views.service_list_view, name='service_list'),
    path('services/<int:service_id>/', views.service_detail_view, name='service_detail'),
    path('book/<int:service_id>/', views.booking_view, name='booking'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment'),
    path('payment/success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('payment/cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('order_summary/<int:booking_id>/', views.order_summary_view, name='order_summary'),
    path('search/', views.search_view, name='search'),
    path('search_suggestions/', views.search_suggestions_view, name='search_suggestions'),
    path('faq/', views.faq_view, name='faq'),
    path('booking/', views.create_booking, name='create_booking'),
    path('booking_success/', views.payment_success, name='booking_success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
