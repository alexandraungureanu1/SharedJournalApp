# Generated by Django 4.1.1 on 2023-05-31 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=journal.models.image_upload_path)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
