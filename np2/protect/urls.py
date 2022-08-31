from django.urls import path
from . import views


app_name = 'protect'

urlpatterns = [
    path('', views.IndexView.as_view(), name='profile'),
]
