# Generated by Django 4.1.3 on 2023-11-11 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequest', '0009_rename_isread_servicerequestchatmessage_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequestchatmessage',
            name='date_time_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
