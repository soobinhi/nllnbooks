# Generated by Django 4.1 on 2022-09-15 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_approval_reason'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='approval_reason',
        ),
    ]
