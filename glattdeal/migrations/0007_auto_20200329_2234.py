# Generated by Django 3.0.4 on 2020-03-29 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glattdeal', '0006_remove_deal_temp_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='deal_desc',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]