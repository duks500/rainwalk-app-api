# Generated by Django 3.1.5 on 2021-01-21 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quate',
            name='pet_name',
            field=models.CharField(default='MAX', max_length=255),
        ),
    ]
