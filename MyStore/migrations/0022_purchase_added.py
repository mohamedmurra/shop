# Generated by Django 4.0.2 on 2022-03-12 14:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0021_purchase_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
