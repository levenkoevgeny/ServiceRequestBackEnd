# Generated by Django 4.1.3 on 2023-11-06 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appUsers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone'),
        ),
    ]
