# Generated by Django 2.2.2 on 2020-03-18 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0011_auto_20200318_0512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestservice',
            old_name='service_name',
            new_name='service_id',
        ),
    ]
