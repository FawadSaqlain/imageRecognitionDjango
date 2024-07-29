# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('view_images/', views.view_images, name='view_images'),
    path('clear_session/', views.clear_session, name='clear_session'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
