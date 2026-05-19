from django.urls import path
from .views import *

urlpatterns = [

    path('',
         department_list,
         name='department_list'),

    path('<int:pk>/',
         department_detail,
         name='department_detail'),
]