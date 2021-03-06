# Generated by Django 3.2.7 on 2021-09-20 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210920_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='shipping_address',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='temporary_address',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
