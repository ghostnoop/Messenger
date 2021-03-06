# Generated by Django 3.2.4 on 2021-08-08 13:02

from django.db import migrations, models
import main.services.models_service


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=main.services.models_service.message_upload_path_create),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
