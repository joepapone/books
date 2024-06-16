from django.urls import path

from apps.accounts.views import Account_LoginView, Account_LogoutView, Account_RegisterView, Account_Profile

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('login/', Account_LoginView.as_view(), name='login'),
    path('logout/', Account_LogoutView.as_view(), name='logout'),
    path('register/', Account_RegisterView.as_view(), name='register'),
    path('password-reset/', 
        PasswordResetView.as_view(
            template_name='accounts/password_reset.html',
            html_email_template_name='accounts/password_reset_email.html'
        ),
        name='password_reset'
    ),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
    path('profile/', Account_Profile.as_view(), name='profile'),
]