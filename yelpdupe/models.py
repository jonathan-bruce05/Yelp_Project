from django.db import models

# Create your models here.

class Review(models.Model):
    place_id = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    rating = models.FloatField()
    text = models.TextField()
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.author_name} - {self.rating}"