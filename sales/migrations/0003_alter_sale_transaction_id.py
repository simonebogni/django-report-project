# Generated by Django 3.2.5 on 2021-07-20 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_position_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]