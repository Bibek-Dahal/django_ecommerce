# Generated by Django 3.2.7 on 2021-09-25 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_productvariationsoptions_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='combination_string',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
