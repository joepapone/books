# Generated by Django 5.1 on 2024-09-03 20:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_price_currency'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='volume_number',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Volume Number'),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('collection', 'volume_number'), name='unique_volume_number_per_collection'),
        ),
    ]
