from django.db import models
from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient


class Report(models.Model):

    # 🔗 RELATIONS
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    # 👤 PATIENT INFO
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)

    # 🩺 VITALS
    bp = models.CharField(max_length=20, blank=True)
    temperature = models.CharField(max_length=20, blank=True)

    # 📋 MEDICAL DETAILS
    diagnosis = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # 📎 ATTACHMENT
    report_file = models.FileField(
        upload_to='reports/',
        null=True,
        blank=True
    )

    # 🕒 TIMESTAMP
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report - {self.patient.user.username} - {self.appointment.token_number}"