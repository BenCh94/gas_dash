# Generated by Django 3.1.2 on 2020-12-30 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_auto_20201230_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='historical_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]