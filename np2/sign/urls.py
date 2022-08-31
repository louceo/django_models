from django.urls import path
from django.contrib.auth import views
from .views import UserRegistrationView, get_staff_access


app_name = 'sign'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', UserRegistrationView.as_view(template_name='sign/signup.html'), name='sign-up'),
    path('upgrade/', get_staff_access, name='upgrade'),
]
