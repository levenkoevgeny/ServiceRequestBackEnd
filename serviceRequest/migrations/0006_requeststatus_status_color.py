# Generated by Django 4.1.3 on 2023-11-07 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceRequest', '0005_alter_servicerequest_date_time_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='requeststatus',
            name='status_color',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Status color'),
        ),
    ]
