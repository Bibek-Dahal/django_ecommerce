# Generated by Django 3.2.7 on 2021-09-28 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_product_image_is_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='main_image',
        ),
    ]
