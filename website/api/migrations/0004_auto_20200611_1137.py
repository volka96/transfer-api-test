# Generated by Django 3.0.3 on 2020-06-11 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200611_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.FloatField(default=0.0, verbose_name='Balance'),
        ),
    ]
