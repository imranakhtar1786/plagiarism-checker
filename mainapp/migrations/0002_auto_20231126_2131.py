# Generated by Django 3.1.2 on 2023-11-26 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
