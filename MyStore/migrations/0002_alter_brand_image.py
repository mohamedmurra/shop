# Generated by Django 4.0 on 2022-02-10 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
