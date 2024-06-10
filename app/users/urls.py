from django.urls import path
from .views import User_LoginView, User_LogoutView, User_RegisterView, User_Profile

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('login/', User_LoginView.as_view(), name='login'),
    path('logout/', User_LogoutView.as_view(), name='logout'),
    path('register/', User_RegisterView.as_view(), name='register'),
    path('password-reset/', 
        PasswordResetView.as_view(
            template_name='users/password_reset.html',
            html_email_template_name='users/password_reset_email.html'
        ),
        name='password_reset'
    ),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('profile/', User_Profile.as_view(), name='profile'),
]