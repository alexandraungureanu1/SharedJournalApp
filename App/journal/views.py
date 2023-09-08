import base64
import io

import numpy as np
import librosa

import requests
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import get_storage_class, default_storage
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from core import settings
from .forms import UploadLibraryImages, UploadLibraryAudioFiles, AddComment
from .models import (
    Post,
    LibraryImages,
    LibraryImagesClassified,
    LibraryAudioFiles,
    LibraryAudioFilesClassified,
    Comments,
)
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from scipy import signal

INSULT_API = "https://europe-west1-test1-385709.cloudfunctions.net/function-3"
FER_API = "https://europe-west1-test1-385709.cloudfunctions.net/function-2"
SER_API = "https://europe-west1-test1-385709.cloudfunctions.net/function-1"


def about(request):
    context = {
        "posts": Post.objects.all()
        .filter(author__id=request.user.id)
        .order_by("-date_posted"),
        "title": "About",
    }
    return render(request, "journal/about.html", context)


@require_http_methods(["POST"])
def upload_view(request, pk):
    post_id = pk
    upload_form_images = UploadLibraryImages(data=request.POST, files=request.FILES)

    if upload_form_images.is_valid():
        library_image = upload_form_images.save(commit=False)
        library_image.post_id = post_id
        library_image.save()
    else:
        messages.error(
            request, "Something went wrong and we couldn't upload your file."
        )

    return redirect("post-detail", pk=post_id)


@require_http_methods(["POST"])
def upload_audio_view(request, pk):
    post_id = pk
    upload_form_audio = UploadLibraryAudioFiles(data=request.POST, files=request.FILES)

    if upload_form_audio.is_valid():
        library_audio = upload_form_audio.save(commit=False)
        library_audio.post_id = post_id
        library_audio.save()
    else:
        messages.error(
            request, "Something went wrong and we couldn't upload your file."
        )
    return redirect("post-detail", pk=post_id)


def analyze_comment(comment):
    json_payload = {"sentence": comment}
    insult_api = INSULT_API
    response = requests.post(insult_api, json=json_payload)

    if response.status_code == 200:
        return response.content.decode()
    else:
        return "Failed API request"


@require_http_methods(["POST"])
@login_required()
def upload_comment(request, pk):
    post_id = pk
    comment_form = AddComment(data=request.POST)

    if comment_form.is_valid():
        comment_content = comment_form.cleaned_data.get("content")
        result_analysis = analyze_comment(comment_content)
        if result_analysis == "True":
            messages.info(
                request, "Your comment was classified as an insult and not posted."
            )
            return redirect("post-detail", pk=post_id)
        comment_addition = comment_form.save(commit=False)
        comment_addition.post_id = post_id
        comment_addition.user_id = request.user.id
        comment_addition.save()

    return redirect("post-detail", pk=post_id)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "journal/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    form_class = UploadLibraryImages
    form_class_audio = UploadLibraryAudioFiles
    form_comment = AddComment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post_id = self.object.id
        post = Post.objects.get(pk=post_id)

        if post.access == "private":
            if self.request.user != post.author:
                raise PermissionDenied

        images = LibraryImages.objects.filter(post__id=post_id).order_by("id")
        all_images = []
        for image in images:
            if LibraryImagesClassified.objects.filter(
                original_image_id=image.id
            ).exists():
                all_images.append(
                    [
                        image,
                        LibraryImagesClassified.objects.get(original_image_id=image.id),
                    ]
                )
            else:
                all_images.append([image, None])

        audio_files = LibraryAudioFiles.objects.filter(post__id=post_id).order_by("id")
        all_audio_files = []

        comments = Comments.objects.filter(post_id=post_id).order_by("id")

        for audio_file in audio_files:
            if LibraryAudioFilesClassified.objects.filter(
                original_audio=audio_file.id
            ).exists():
                all_audio_files.append(
                    [
                        audio_file,
                        LibraryAudioFilesClassified.objects.get(
                            original_audio=audio_file.id
                        ),
                    ]
                )
            else:
                all_audio_files.append([audio_file, None])

        x_icon_path = "icons/x_icon.png"
        analyze_icon_path = "icons/analyze_icon.png"
        x_icon = default_storage.url(x_icon_path)
        analyze_icon = default_storage.url(analyze_icon_path)
        context["upload_form"] = self.get_form()
        context["upload_form_audio"] = self.get_audio_form()
        context["all_images"] = all_images
        context["x_icon"] = x_icon
        context["analyze_icon"] = analyze_icon
        context["all_audio_files"] = all_audio_files
        context["comment_form"] = self.get_comment_form()
        context["access"] = post.access
        context["comments"] = comments
        return context

    def get_form(self):
        form = self.form_class()
        return form

    def get_audio_form(self):
        form = self.form_class_audio()
        return form

    def get_comment_form(self):
        form = self.form_comment()
        return form


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "access"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "journal/user_posts.html"  
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


def delete_image(request, image_id):
    image = LibraryImages.objects.filter(pk=image_id).first()
    if image:
        storage = settings.DEFAULT_FILE_STORAGE
        storage_backend = get_storage_class(storage)()
        storage_backend.delete(image.image.name)
        image.delete()

    return redirect("journal-home")


def delete_audio(request, audio_id):
    audio_file = LibraryAudioFiles.objects.get(pk=audio_id)
    if audio_file:
        storage = settings.DEFAULT_FILE_STORAGE
        storage_backend = get_storage_class(storage)()
        storage_backend.delete(audio_file.audio.name)
        audio_file.delete()

    return redirect("journal-home")


def analyze_image(request, image_id):
    image = LibraryImages.objects.filter(pk=image_id).first()

    if image:
        image_url = image.image.url
        response = requests.get(image_url)
        image_data = response.content

        base64_image = base64.b64encode(image_data).decode("utf-8")
        json_payload = {"image": base64_image}
        fer_api = FER_API
        response = requests.post(fer_api, json=json_payload)

        if response.status_code == 200:
            library_image = LibraryImages.objects.get(id=image_id)

            image_data = response.content
            my_model = LibraryImagesClassified(original_image=library_image)
            my_model.image.save("image.jpg", ContentFile(image_data))
            my_model.save()

        else:
            # API request failed
            print("API request failed with status code:", response.status_code)
    return redirect("journal-home")


def extract_mfcc(audio_file):
    audio_data, sr = librosa.load(audio_file)
    target_sample_rate = 22050
    if sr != target_sample_rate:
        audio_data = signal.resample_poly(audio_file, target_sample_rate, sr)

    mfccs = np.mean(
        librosa.feature.mfcc(y=audio_data, sr=target_sample_rate, n_mfcc=40).T, axis=0
    )
    return mfccs


def analyze_audio(request, audio_id):
    audio = LibraryAudioFiles.objects.get(pk=audio_id)
    emotions_dict = {
        "1": "neutral",
        "2": "calm",
        "3": "happy",
        "4": "sad",
        "5": "angry",
        "6": "fearful",
        "7": "disgust",
        "8": "surprised",
    }

    if audio:
        print("here")
        mfccs = (extract_mfcc(audio.audio)).tolist()
        json_payload = {"mfccs_features": mfccs}
        ser_api = SER_API
        response = requests.post(ser_api, json=json_payload)

        if response.status_code == 200:
            print(response.content)
            library_audio = LibraryAudioFiles.objects.get(id=audio_id)

            if LibraryAudioFilesClassified.objects.filter(
                original_audio=audio_id
            ).exists():
                existing_instance = LibraryAudioFilesClassified.objects.get(
                    original_audio=audio_id
                )
                existing_instance.delete()
            classification_data = response.content.decode("utf-8")
            class_audio_model = LibraryAudioFilesClassified(
                original_audio=library_audio
            )
            class_audio_model.classification_result = emotions_dict[
                str(classification_data)
            ]
            class_audio_model.save()
        else:
            # API request failed
            print("API request failed with status code:", response.status_code)

    return redirect("journal-home")


@login_required
def capture_photo(request, pk):
    if request.method == "POST":
        print(f"photo captured {pk}")
        photo_data = request.POST.get("photo")
        if photo_data:
            format, imgstr = photo_data.split(";base64,")
            ext = format.split("/")[-1]
            photo = ContentFile(base64.b64decode(imgstr), name=f"photo.{ext}")

            img = Image.open(photo)
            resized_photo = io.BytesIO()
            img.save(resized_photo, format="JPEG")
            resized_image = InMemoryUploadedFile(
                resized_photo,
                None,
                "image.jpg",
                "image/jpeg",
                resized_photo.getbuffer().nbytes,
                None,
            )

            my_model = LibraryImages(post_id=pk)
            my_model.image.save("image.jpg", resized_image)
            my_model.save()
        return JsonResponse({"redirect_url": "/journal-home/"})
    else:
        return render(request, "journal/capture_photo.html")


@login_required
def record_audio(request, pk):
    if request.method == "POST":
        print(f"audio recorded {pk}")

        if request.FILES:
            audio_file = request.FILES.get("audio")

            audio_model = LibraryAudioFiles(post_id=pk)
            audio_model.audio.save("audio_file.wav", audio_file)
            audio_model.save()
        return JsonResponse({"redirect_url": "/journal-home/"})

    else:
        return render(request, "journal/capture_photo.html")
