# Generated by Django 4.0.2 on 2022-03-07 10:14

import MyStore.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyStore', '0009_alter_wherehouse_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wherehouse',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wherehouse',
            name='status',
        ),
        migrations.AddField(
            model_name='wherehouse',
            name='transfere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MyStore.product'),
        ),
        migrations.CreateModel(
            name='Transfere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=MyStore.models.tansaction_id_genrater, max_length=10, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('shupping_charge', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('full', ' full'), ('empty', ' empty'), ('Partial\t', ' Partial\t'), ('Pending', ' Pending')], default='Partial', max_length=20)),
                ('note', models.TextField(blank=True, null=True)),
                ('give_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lucation_to', to='MyStore.wherehouse')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='MyStore.wherehouse')),
                ('take_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lucation_from', to='MyStore.wherehouse')),
            ],
        ),
    ]