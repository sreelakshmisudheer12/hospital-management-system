from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/',
         patient_dashboard,
         name='patient_dashboard'),
]