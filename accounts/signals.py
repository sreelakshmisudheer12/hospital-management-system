from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from doctors.models import Doctor
from patients.models import Patient


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:

        if hasattr(instance, "role"):

            if instance.role == "DOCTOR":
                Doctor.objects.create(user=instance)

            elif instance.role == "PATIENT":
                Patient.objects.create(user=instance)