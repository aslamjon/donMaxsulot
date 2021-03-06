# Generated by Django 3.2.5 on 2021-07-09 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mainBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeOfProduct', models.TextField()),
                ('kg', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('totalSum', models.IntegerField(blank=True, default=0)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('chackbox', models.BooleanField(default=False)),
            ],
        ),
    ]
