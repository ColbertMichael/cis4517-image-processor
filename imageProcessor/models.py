from django.db import models

# Create your models here.

#table to handle uploaded images
class ImageTable(models.Model):
    uploadedImage = models.ImageField(upload_to='uploads/')
    filteredImage = models.ImageField(upload_to='processedImage/', null=True, blank=True)
    uploadedAt = models.DateTimeField(auto_now=True)
