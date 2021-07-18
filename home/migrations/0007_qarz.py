# Generated by Django 3.2.5 on 2021-07-13 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210713_0121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qarz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeOfProduct', models.TextField()),
                ('kg', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('qarzSum', models.IntegerField(default=0)),
                ('qarzDate', models.DateField(null=True)),
                ('byWhom', models.TextField(default='')),
                ('changed', models.BooleanField(default=False)),
            ],
        ),
    ]
