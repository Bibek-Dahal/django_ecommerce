# Generated by Django 3.2.7 on 2021-09-26 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_productinventory_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='store.productvariationvalue'),
        ),
    ]
