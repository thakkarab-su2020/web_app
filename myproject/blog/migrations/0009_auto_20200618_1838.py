# Generated by Django 3.0.6 on 2020-06-18 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookimage',
            name='book',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='blog.Book'),
        ),
        migrations.AlterField(
            model_name='bookimage',
            name='image',
            field=models.ImageField(upload_to='pictures'),
        ),
    ]
