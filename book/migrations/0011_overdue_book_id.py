# Generated by Django 4.1.1 on 2022-09-27 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_alter_rental_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='overdue',
            name='book_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='book_overdue', to='book.book'),
            preserve_default=False,
        ),
    ]