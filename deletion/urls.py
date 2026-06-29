from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('delete_account'), name='home'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
