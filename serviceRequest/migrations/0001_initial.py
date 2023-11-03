# Generated by Django 4.1.3 on 2023-11-03 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(verbose_name='Location')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_created', models.DateTimeField(auto_created=True, verbose_name='Date and time created')),
                ('address', models.TextField(verbose_name='Address')),
                ('phone_number', models.CharField(max_length=100, verbose_name='Phone')),
                ('request_description', models.TextField(verbose_name='Description')),
                ('date_time_edited', models.DateTimeField(auto_now=True, verbose_name='Date and time edited')),
                ('executor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executor', to=settings.AUTH_USER_MODEL, verbose_name='Executor')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceRequest.location', verbose_name='Location')),
                ('request_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Request sender')),
                ('request_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceRequest.requeststatus', verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
                'ordering': ('id',),
            },
        ),
    ]
