# Generated by Django 4.1.3 on 2023-11-10 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequest', '0008_servicerequestchatmessage_isread'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicerequestchatmessage',
            old_name='isRead',
            new_name='is_read',
        ),
    ]
