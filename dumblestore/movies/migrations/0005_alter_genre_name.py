# Generated by Django 4.0.2 on 2022-02-08 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_user_options_alter_movie_genres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
