# Generated by Django 4.0.2 on 2022-10-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_acount_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='acount',
            name='position',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]