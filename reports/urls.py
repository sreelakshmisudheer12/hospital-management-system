from django.urls import path
from .views import add_report, view_reports, download_report

urlpatterns = [
    path('add/<int:appointment_id>/', add_report, name='add_report'),
    path('view/', view_reports, name='view_reports'),
    path('download/<int:report_id>/', download_report, name='download_report'),

]