from django.db import models

# Create your models here.

class Composition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=100)
    limestone_percentage=models.FloatField()
    sandstone_percentage=models.FloatField()
    shale_percentage=models.FloatField()
    unknown_percentage=models.FloatField()
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

