# Generated by Django 3.0.5 on 2020-04-19 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_personcollection_last_successful_fetch_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personcollection',
            name='last_successful_fetch_page',
            field=models.IntegerField(default=0),
        ),
    ]
