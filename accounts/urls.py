# accounts/urls.py
from django.urls import path
from .views import ProfileView

app_name = 'accounts'

urlpatterns = [
    # Login and Logout are handled by django-allauth via 'allauth.urls' in config/urls.py
    path('profile/', ProfileView.as_view(), name='profile'),
]