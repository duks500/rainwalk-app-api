# Generated by Django 3.1.5 on 2021-01-15 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_pet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='pet_age',
            field=models.PositiveIntegerField(),
        ),
    ]
