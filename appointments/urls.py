from django.urls import path
from . import views
from reports.views import add_report

urlpatterns = [

    path('search/', views.search_doctors, name='search_doctors'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('history/', views.appointment_history, name='appointment_history'),
    path('cancel/<int:pk>/', views.cancel_appointment, name='cancel_appointment'),
    path('reschedule/<int:pk>/', views.reschedule_appointment, name='reschedule_appointment'),

    path('doctor/', views.doctor_appointments, name='doctor_appointments'),

    path('approve/<int:pk>/', views.approve_appointment, name='approve_appointment'),
    path('reject/<int:pk>/', views.reject_appointment, name='reject_appointment'),
    path('complete/<int:pk>/', views.complete_appointment, name='complete_appointment'),

    path('download/<int:pk>/', views.download_appointment, name='download_appointment'),

    path('reports/add/<int:appointment_id>/', add_report, name='add_report'),

    path('delete/<int:pk>/', views.delete_appointment, name='delete_appointment'),

    
    path('appointment/success/', views.appointment_success, name='appointment_success')
]