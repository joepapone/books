# Generated by Django 5.0.6 on 2024-06-25 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_category_collection_section_alter_author_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='authors',
            new_name='author',
        ),
    ]
