# Generated by Django 3.0.5 on 2020-04-20 07:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0009_auto_20200420_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personcollection',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]