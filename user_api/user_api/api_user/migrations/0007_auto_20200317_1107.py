# Generated by Django 2.2.2 on 2020-03-17 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0006_auto_20200317_1041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='service_name',
            new_name='service_id',
        ),
    ]
