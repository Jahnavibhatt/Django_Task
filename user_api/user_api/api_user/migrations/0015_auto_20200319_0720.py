# Generated by Django 2.2.2 on 2020-03-19 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0014_auto_20200318_0600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='consumer',
        ),
    ]
