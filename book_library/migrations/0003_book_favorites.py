# Generated by Django 3.0.5 on 2020-05-01 18:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book_library', '0002_auto_20200430_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='book_favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]