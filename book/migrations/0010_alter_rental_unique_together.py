# Generated by Django 4.1.1 on 2022-09-26 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_overdue'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rental',
            unique_together={('id', 'book_id')},
        ),
    ]
