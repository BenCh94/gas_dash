# Generated by Django 3.1.2 on 2020-12-30 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20200504_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='benchmark_data',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='benchmark_name',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='benchmark_ticker',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='benchmark_object',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.ticker'),
        ),
    ]
