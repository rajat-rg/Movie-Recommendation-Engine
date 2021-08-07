from django.db import models

# Create your models here.
class movies_model(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=200)
    tags = models.TextField(max_length=5100)
    def __str__(self):
        return self.title