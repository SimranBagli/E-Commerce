# Generated by Django 3.0.4 on 2020-03-30 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glattdeal', '0011_auto_20200330_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='glattdeal.Category'),
        ),
    ]
