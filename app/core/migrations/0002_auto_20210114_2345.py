# Generated by Django 3.1.5 on 2021-01-14 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='0000000000', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='zipcode',
            field=models.CharField(default='00000', max_length=5),
        ),
    ]
