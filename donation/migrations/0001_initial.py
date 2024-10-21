# Generated by Django 5.1.2 on 2024-10-21 07:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('tagline', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('end_date', models.DateTimeField()),
                ('banner_image', models.ImageField(upload_to='uploads/')),
                ('cover_image', models.ImageField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cause', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation.cause')),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
