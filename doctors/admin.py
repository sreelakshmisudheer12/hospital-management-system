from django.contrib import admin

from .models import Doctor, DoctorSchedule


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = [

        'user',
        'doctor_id',
        'department',
        'specialization',
        'approved'
    ]

    list_filter = [

        'approved',
        'department'
    ]

    search_fields = [

        'user__username',
        'specialization',
        'doctor_id'
    ]


admin.site.register(DoctorSchedule)