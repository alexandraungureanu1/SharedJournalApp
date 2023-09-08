from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image


def image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_name = f'profile_{instance.id}.{ext}'
    return os.path.join('profile_pics/', unique_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to=image_upload_path)

    def __str__(self):
        return f'{self.user.username} Profile'
