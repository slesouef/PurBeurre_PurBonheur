# Generated by Django 3.0.7 on 2020-06-22 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='code',
            field=models.BigIntegerField(null=True),
        ),
    ]
