# Generated by Django 3.2.5 on 2021-07-14 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20210714_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qarz',
            name='oxirgiQarzBerganVaqti',
        ),
        migrations.RemoveField(
            model_name='qarz',
            name='qarzSum',
        ),
        migrations.RemoveField(
            model_name='qarz',
            name='totalLend',
        ),
        migrations.AlterField(
            model_name='inputqarz',
            name='byWhom',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='inputqarz',
            name='qarzSum',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='inputqarz',
            name='totalLend',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='qarz',
            name='byWhom',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='qarz',
            name='changed',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='qarz',
            name='debt',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='qarz',
            name='kg',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='qarz',
            name='orginalPrice',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='qarz',
            name='price',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='qarz',
            name='typeOfProduct',
            field=models.TextField(null=True),
        ),
    ]