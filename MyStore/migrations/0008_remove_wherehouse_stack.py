# Generated by Django 4.0.2 on 2022-03-07 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0007_wherehouse_date_add'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wherehouse',
            name='stack',
        ),
    ]