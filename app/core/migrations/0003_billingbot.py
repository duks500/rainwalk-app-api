# Generated by Django 3.1.5 on 2021-01-26 22:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210121_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingBot',
            fields=[
                ('bot_id', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]