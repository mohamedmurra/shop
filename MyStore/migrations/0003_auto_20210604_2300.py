# Generated by Django 3.2.3 on 2021-06-04 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0002_customer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='sim_config',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('image1', models.ImageField(upload_to='sim_config')),
                ('image2', models.ImageField(upload_to='sim_config')),
            ],
        ),
        migrations.AddField(
            model_name='catagory',
            name='slug',
            field=models.SlugField(default=1),
        ),
        migrations.AlterField(
            model_name='brand',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='catagory',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='repairs',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
