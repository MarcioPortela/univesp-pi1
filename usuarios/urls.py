from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),  # Account page
    path('account/orders/', views.orders, name='orders'),
    path('account/edit/', views.edit_profile, name='edit_profile'),
    path('account/password/', views.change_password, name='change_password'),
    path('account/favorites/', views.favorites, name='favorites'),
    path('account/delete/', views.delete_account, name='delete_account'),
]