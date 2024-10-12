from django.db import models

# Create your models here.

#table to handle uploaded images
class ImageTable(models.Model):
    uploadedImage = models.ImageField(upload_to='media/uploads/')
    filteredImage = models.ImageField(upload_to='media/processedImage/', null=True, blank=True)
    uploadedAt = models.DateTimeField(auto_now=True)
