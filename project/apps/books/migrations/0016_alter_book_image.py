# Generated by Django 5.0.6 on 2024-06-28 23:25

import apps.books.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0015_delete_uploadedfile_remove_book_publisher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default='book.png', null=True, upload_to=apps.books.models.upload_to_books, verbose_name=''),
        ),
    ]
