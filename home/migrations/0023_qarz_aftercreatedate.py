# Generated by Django 3.2.5 on 2021-07-14 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_payagent_lastpayagent'),
    ]

    operations = [
        migrations.AddField(
            model_name='qarz',
            name='afterCreateDate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
