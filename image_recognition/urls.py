from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import upload_image, view_images

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('images/', view_images, name='view_images'),
]
