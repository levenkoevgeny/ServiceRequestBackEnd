# Generated by Django 4.1.3 on 2023-11-06 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequest', '0004_remove_servicerequest_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerequest',
            name='date_time_created',
            field=models.DateTimeField(auto_now=True, verbose_name='Date and time created'),
        ),
    ]
