# Generated by Django 4.0.2 on 2022-03-12 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0019_expense_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='Document',
            field=models.FileField(blank=True, null=True, upload_to='product/files'),
        ),
    ]
