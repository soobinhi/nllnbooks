# Generated by Django 4.1 on 2022-09-14 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_user_user_role_user_is_staff_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
    ]
