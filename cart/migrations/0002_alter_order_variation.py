# Generated by Django 3.2.7 on 2021-09-28 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='variation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]