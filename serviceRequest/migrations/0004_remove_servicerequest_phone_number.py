# Generated by Django 4.1.3 on 2023-11-06 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequest', '0003_alter_servicerequest_request_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicerequest',
            name='phone_number',
        ),
    ]
