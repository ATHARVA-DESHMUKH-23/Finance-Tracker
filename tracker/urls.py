# tracker/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_entry, name='add_entry'),
    path('signup/', views.signup_view, name='signup'),
    path('extract_bill_text/', views.extract_bill_text_view, name='upload_bill'),
]
