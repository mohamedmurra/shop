# Generated by Django 4.0.2 on 2022-03-06 22:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0006_remove_wherehouse_lucation_wherehouse_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wherehouse',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
