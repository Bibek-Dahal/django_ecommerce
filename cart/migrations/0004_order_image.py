# Generated by Django 3.2.7 on 2021-09-30 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_alter_product_description'),
        ('cart', '0003_alter_order_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product_image'),
        ),
    ]
