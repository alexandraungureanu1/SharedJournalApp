from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView

)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='journal-home'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('users/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('myposts/', views.about, name='journal-about'),
    path('posts/upload/<int:pk>/', views.upload_view, name='library-images-upload'),
    path('posts/upload_audio/<int:pk>/', views.upload_audio_view, name='library-audio-upload'),
    path('posts/image/delete/<int:image_id>/', views.delete_image, name='delete-image'),
    path('posts/image/analyze/<int:image_id>/', views.analyze_image, name='analyze-image'),
    path('posts/audio/analyze/<int:audio_id>/', views.analyze_audio, name='analyze-audio'),
    path('posts/audio/delete/<int:audio_id>/', views.delete_audio, name='delete-audio'),
    path('posts/capture_photo/<int:pk>/', views.capture_photo, name='capture_photo'),
    path('posts/record_audio/<int:pk>/', views.record_audio, name='record-audio'),
    path('posts/comment/<int:pk>/', views.upload_comment, name='upload-comment'),
]
