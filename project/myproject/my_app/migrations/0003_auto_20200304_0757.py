# Generated by Django 2.2 on 2020-03-04 07:57

from django.db import migrations
import my_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_order_quntity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Quntity',
            field=my_app.models.ListField(),
        ),
    ]
