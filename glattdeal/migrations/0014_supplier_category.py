# Generated by Django 3.0.4 on 2020-03-30 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('glattdeal', '0013_remove_supplier_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='category',
            field=models.CharField(max_length=10, null=True),
        ),
    ]