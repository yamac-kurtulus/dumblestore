# Generated by Django 4.0.2 on 2022-02-06 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_add_admin_user_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='first_name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='last_name'),
        ),
    ]
