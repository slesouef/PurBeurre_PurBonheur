# Generated by Django 2.2 on 2019-05-14 19:29

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='myuser',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]