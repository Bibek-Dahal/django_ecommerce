# Generated by Django 3.2.7 on 2021-09-28 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20210928_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_image',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
