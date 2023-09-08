from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LibraryImages, LibraryAudioFiles, Comments


class UploadLibraryImages(forms.ModelForm):
    class Meta:
        model = LibraryImages
        fields = ["image"]


class UploadLibraryAudioFiles(forms.ModelForm):
    class Meta:
        model = LibraryAudioFiles
        fields = ["audio"]


class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Write a comment...",
                    "rows": 1,
                    "class": "rounded-grey-textarea",
                }
            ),
        }
