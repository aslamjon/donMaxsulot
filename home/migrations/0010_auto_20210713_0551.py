# Generated by Django 3.2.5 on 2021-07-13 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_qarz_totalsum'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputQarz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qarzSum', models.IntegerField(default=0)),
                ('oxirgiQarzBerganVaqti', models.DateField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='qarz',
            name='oxirgiQarzBerganVaqti',
        ),
        migrations.RemoveField(
            model_name='qarz',
            name='qarzSum',
        ),
    ]
