# Generated by Django 3.0.5 on 2020-04-30 03:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book_library', '0002_auto_20200430_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
