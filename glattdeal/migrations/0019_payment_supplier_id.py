# Generated by Django 3.0.4 on 2020-04-02 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('glattdeal', '0018_auto_20200330_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='supplier_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='glattdeal.Supplier'),
        ),
    ]
