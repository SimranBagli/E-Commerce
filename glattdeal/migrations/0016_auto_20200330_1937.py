# Generated by Django 3.0.4 on 2020-03-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glattdeal', '0015_auto_20200330_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='category',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
