# Generated by Django 4.0.2 on 2022-07-22 09:55

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_acount_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acount',
            name='image',
            field=models.ImageField(null=True, upload_to=account.models.uplaod_lucation),
        ),
    ]
