# Generated by Django 3.2.7 on 2021-09-25 05:42

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_productinventory_sku'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productvariationsoptions',
            options={},
        ),
        migrations.AlterField(
            model_name='productvariationsoptions',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=models.CharField(max_length=100, unique=True), unique=True),
        ),
    ]
