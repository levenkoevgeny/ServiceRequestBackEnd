# Generated by Django 4.1.3 on 2023-11-15 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequest', '0012_rename_isblockchat_requeststatus_is_block_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicerequestchatmessage',
            name='is_read',
        ),
    ]