# Generated by Django 4.0.2 on 2022-03-12 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0020_alter_purchase_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='status',
            field=models.CharField(choices=[('recived', ' recived'), ('Conseld', ' Conseld'), ('Partial\t', ' Partial\t'), ('Pending', ' Pending')], default='Partial', max_length=20),
        ),
    ]