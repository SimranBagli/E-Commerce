# Generated by Django 3.0.4 on 2020-03-30 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glattdeal', '0008_auto_20200330_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='supplier_endtime',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='supplier_starttime',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
