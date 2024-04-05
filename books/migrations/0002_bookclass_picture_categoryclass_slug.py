# Generated by Django 5.0.2 on 2024-04-04 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookclass',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='book/media/uploads'),
        ),
        migrations.AddField(
            model_name='categoryclass',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
