from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = [
        'appointment_id',
        'patient',
        'doctor',
        'appointment_date',
        
        'status',
        'payment_status'
    ]

    list_filter = [
        'status',
        'payment_status',
        'appointment_date'
    ]

    search_fields = [
        'patient__user__username',
        'doctor__user__username'
    ]

    ordering = [
        '-created_at'
    ]