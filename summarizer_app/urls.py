from django.urls import path
from .views import UploadFile

urlpatterns = [
    path('upload-file/', UploadFile.as_view(), name='upload-file'),
]