# Generated by Django 4.1.1 on 2022-09-30 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.TextField(default='https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg'),
        ),
    ]
