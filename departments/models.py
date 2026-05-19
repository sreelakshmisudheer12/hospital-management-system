from django.db import models

# Create your models here.
from django.db import models

class Department(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='departments/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name