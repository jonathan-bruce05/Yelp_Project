from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add custom fields here if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Override the groups and user_permissions fields to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Add this related_name to avoid clashes
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Add this related_name to avoid clashes
        blank=True,
    )

class Review(models.Model):
    place_id = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    rating = models.FloatField()
    text = models.TextField()
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.author_name} - {self.rating}"