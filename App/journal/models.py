from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import os


class Post(models.Model):
    ACCESS_CHOICES = [
        ("private", "Private"),
        ("public", "Public"),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.CharField(default="public", max_length=10, choices=ACCESS_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


def image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    counter = 0
    if LibraryImages.objects.exists():
        counter = LibraryImages.objects.last().id + 1
    unique_name = f"libimg_{instance.post_id}_{counter}.{ext}"
    return os.path.join("library_images/", unique_name)


class LibraryImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_path)

    def __str__(self):
        return f"{self.post.id} Post"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.id})


def image_upload_path_classified(instance, filename):
    return instance.get_image_upload_path(filename)


class LibraryImagesClassified(models.Model):
    original_image = models.ForeignKey(LibraryImages, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_path_classified)

    def __str__(self):
        return f"{self.original_image.id} LibraryImages"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.original_image.post_id})

    def get_image_upload_path(self, filename):
        ext = filename.split(".")[-1]
        counter = 0

        if LibraryImagesClassified.objects.filter(
            original_image=self.original_image
        ).exists():
            existing_instance = LibraryImagesClassified.objects.get(
                original_image=self.original_image
            )
            existing_instance.delete()
        if LibraryImagesClassified.objects.exists():
            counter = LibraryImagesClassified.objects.last().id + 1

        unique_name = f"libimgcla_{counter}.{ext}"
        return os.path.join("library_images_classified/", unique_name)


def audio_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    counter = 0
    if LibraryAudioFiles.objects.exists():
        counter = LibraryAudioFiles.objects.last().id + 1
    unique_name = f"libaudio_{instance.post_id}_{counter}.{ext}"
    return os.path.join("library_audio_files/", unique_name)


class LibraryAudioFiles(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    audio = models.FileField(upload_to=audio_upload_path)

    def __str__(self):
        return f"{self.post.id} Post"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.id})


class LibraryAudioFilesClassified(models.Model):
    original_audio = models.ForeignKey(LibraryAudioFiles, on_delete=models.CASCADE)
    classification_result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.original_audio.id} Post"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.original_audio.post.id})


class Shares(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.id} Post"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.id})


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(default="", max_length=300)

    def __str__(self):
        return f"{self.post.id} Post"

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.id})
