from django.urls import path
from apps.core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path("mine/", views.MyView.as_view(), name="my-view"),
]