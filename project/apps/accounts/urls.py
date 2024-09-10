from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

# Application modules
from apps.accounts import views

urlpatterns = [
    path('register/', views.AccountRegisterView.as_view(), name='register'),
    path('login/', views.AccountLoginView.as_view(), name='login'),
    path('logout/', views.AccountLogoutView.as_view(), name='logout'),
    path('profile/', views.AccountProfileUpdateView.as_view(), name='profile'),
    path('password-reset/', 
        PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            html_email_template_name='accounts/password_reset_email.html'
            ), name='password_reset'
    ),
    path('password-reset-confirm/<uidb64>/<token>/', 
         PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
             ), name='password_reset_confirm'),
    path('password-reset/done/', 
         PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
             ), name='password_reset_done'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
             ), name='password_reset_complete'),
]