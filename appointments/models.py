from django.db import models, transaction
from django.db.models import Max
import uuid

from doctors.models import Doctor
from patients.models import Patient


class Appointment(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )

    appointment_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    token_number = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateField()
    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    payment_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date', 'token_number']

    def save(self, *args, **kwargs):

        if self._state.adding and not self.token_number:

            with transaction.atomic():

                last_token = (
                    Appointment.objects
                    .filter(
                        doctor=self.doctor,
                        appointment_date=self.appointment_date
                    )
                    .aggregate(Max('token_number'))['token_number__max']
                )

                self.token_number = (last_token or 0) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.user.username} - {self.doctor.user.username} - Token {self.token_number}"