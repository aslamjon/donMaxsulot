# Generated by Django 3.2.5 on 2021-07-12 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210712_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainbase',
            name='changed',
            field=models.BooleanField(default=False),
        ),
    ]
