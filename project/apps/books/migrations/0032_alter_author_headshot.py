# Generated by Django 5.0.6 on 2024-06-30 14:56

import apps.books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0031_alter_author_headshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='headshot',
            field=models.ImageField(default='author.png', null=True, upload_to=apps.books.models.upload_to_authors),
        ),
    ]
