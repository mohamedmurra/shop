# Generated by Django 4.0.2 on 2022-07-22 09:55

import Blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_alter_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(null=True, upload_to=Blog.models.uplaod_lucation),
        ),
    ]
