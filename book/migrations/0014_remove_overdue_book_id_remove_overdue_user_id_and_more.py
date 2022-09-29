# Generated by Django 4.1.1 on 2022-09-29 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_alter_rental_rental_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='overdue',
            name='book_id',
        ),
        migrations.RemoveField(
            model_name='overdue',
            name='user_id',
        ),
        migrations.AddField(
            model_name='overdue',
            name='rental_id',
            field=models.ForeignKey(default=68, on_delete=django.db.models.deletion.CASCADE, related_name='rental_overdue', to='book.rental'),
            preserve_default=False,
        ),
    ]