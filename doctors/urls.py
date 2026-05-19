from django.urls import path
from .views import *

urlpatterns = [

    path('', doctor_list, name='doctor_list'),

    path('<int:pk>/', doctor_detail, name='doctor_detail'),

    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),

    path('profile/', doctor_profile, name='doctor_profile'),

    path('update/', update_doctor_profile, name='update_doctor_profile'),

    path('schedule/add/', add_schedule, name='add_schedule'),

    path('schedule/delete/<int:pk>/', delete_schedule, name='delete_schedule'),

    # 🔥 API FOR TIME SLOTS (FIXED)
    path(
        'api/doctor-slots/<int:doctor_id>/<str:date>/',
        get_available_slots,
        name='doctor_slots'
    ),
]