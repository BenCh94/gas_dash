# Generated by Django 2.2.10 on 2020-05-04 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_auto_20200502_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='palette',
            field=models.TextField(choices=[('dark_knight', 'Dark Knight'), ('ice_man', 'Ice Man'), ('bright_eyes', 'Bright Eyes'), ('gun_metal', 'Gun Metal'), ('acid_rap', 'Acid Rap')], default='gun_metal'),
        ),
    ]