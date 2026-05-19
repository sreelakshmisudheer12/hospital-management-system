from django.db import models

from accounts.models import CustomUser
from departments.models import Department


class Doctor(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    doctor_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    approved = models.BooleanField(
        default=False
    )

    photo = models.ImageField(
        upload_to='doctors/',
        blank=True,
        null=True
    )

    specialization = models.CharField(
        max_length=200
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='doctors'
    )

    experience = models.PositiveIntegerField(
        default=0
    )

    contact = models.CharField(
        max_length=20
    )

    consultation_fee = models.DecimalField(
    max_digits=6,
    decimal_places=2,
    null=True,
    blank=True,
    default=0
)
    bio = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Dr. {self.user.username}"


from django.db import models
from doctors.models import Doctor


class DoctorSchedule(models.Model):

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='schedules'
    )

    day = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['day', 'start_time']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'day', 'start_time', 'end_time'],
                name='unique_doctor_schedule_slot'
            )
        ]

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day} ({self.start_time} - {self.end_time})"