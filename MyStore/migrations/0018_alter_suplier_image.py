# Generated by Django 4.0.2 on 2022-03-12 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0017_alter_suplier_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suplier',
            name='image',
            field=models.ImageField(upload_to='Supplier'),
        ),
    ]