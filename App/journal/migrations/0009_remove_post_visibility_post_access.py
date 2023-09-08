# Generated by Django 4.1.1 on 2023-06-06 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0008_shares'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='visibility',
        ),
        migrations.AddField(
            model_name='post',
            name='access',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public')], default='public', max_length=10),
        ),
    ]
