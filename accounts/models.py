from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    token = models.UUIDField(default=uuid.uuid4,
                             editable=False,
                             unique=True)

    def __str__(self):
        return self.username