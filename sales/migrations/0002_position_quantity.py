# Generated by Django 3.2.5 on 2021-07-20 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]