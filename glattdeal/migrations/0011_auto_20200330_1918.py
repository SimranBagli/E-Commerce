# Generated by Django 3.0.4 on 2020-03-30 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glattdeal', '0010_supplier_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='supplier_contact',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='supplier_details',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]
