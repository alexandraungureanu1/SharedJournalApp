# Generated by Django 4.1.1 on 2023-06-13 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0010_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='content',
            field=models.CharField(default='', max_length=300),
        ),
    ]
