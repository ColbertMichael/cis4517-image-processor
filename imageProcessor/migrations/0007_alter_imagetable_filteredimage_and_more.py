# Generated by Django 5.1.1 on 2024-10-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageProcessor', '0006_rename_image_imagetable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagetable',
            name='filteredImage',
            field=models.ImageField(blank=True, null=True, upload_to='media/processedImage/'),
        ),
        migrations.AlterField(
            model_name='imagetable',
            name='uploadedImage',
            field=models.ImageField(upload_to='media/uploads/'),
        ),
    ]
