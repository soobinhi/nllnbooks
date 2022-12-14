# Generated by Django 4.1.1 on 2022-09-21 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0004_alter_book_book_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rental',
            name='extension_date',
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserve_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_reserve', to='book.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reserve', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
