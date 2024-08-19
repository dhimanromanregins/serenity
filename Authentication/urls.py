from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('request_otp/', views.request_otp, name='request_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
]
