# Generated by Django 3.2.5 on 2021-07-14 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_inputqarz_payagent'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('who', models.TextField(default='')),
                ('payAgent', models.IntegerField(default=0, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='inputqarz',
            name='payAgent',
        ),
    ]
