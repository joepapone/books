# Generated by Django 5.0.6 on 2024-08-05 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0045_remove_rating_book_book_rating_alter_book_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='status',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='book',
            name='stutus',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
    ]
