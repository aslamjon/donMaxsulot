# Generated by Django 3.2.5 on 2021-07-14 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_qarz_orginalprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='qarz',
            name='oxirgiQarzBerganVaqti',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='qarz',
            name='qarzSum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='qarz',
            name='totalLend',
            field=models.IntegerField(default=0),
        ),
    ]
