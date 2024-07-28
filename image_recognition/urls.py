# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from image_recognition.views import upload_image, view_images

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('view_images/', view_images, name='view_images'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
