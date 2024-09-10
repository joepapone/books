# Generated by Django 5.1 on 2024-09-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_price_price_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('JPY', 'Japanese Yen'), ('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('CHF', 'Swiss Franc'), ('CNY', 'Chinese Yuan'), ('SEK', 'Swedish Krona'), ('NZD', 'New Zealand Dollar')], default='EUR', max_length=3, verbose_name='Currency'),
        ),
    ]