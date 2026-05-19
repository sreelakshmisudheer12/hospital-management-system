from django.db import models
from accounts.models import CustomUser

class Patient(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username