# views.py
from django.conf import settings
from django.shortcuts import render
from .prediction_functions import output , img_paths # Ensure the correct function is imported
import os

def upload_image(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        title = request.POST['title']
        images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        file_path = os.path.join(images_dir, uploaded_file.name)
        img_paths.append(file_path)  # Add the image path to img_paths for prediction

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        with open(os.path.join(images_dir, 'images.txt'), 'a') as file:
            file.write(f"{title},{uploaded_file.name}\n")

        # return redirect('view_images')
    return render(request, 'upload.html')

def view_images(request):
    images = []
    images_file_path = os.path.join(settings.MEDIA_ROOT, 'images', 'images.txt')

    if os.path.exists(images_file_path):
        with open(images_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                title, filename = line.strip().split(',')
                images.append({'title': title, 'filename': filename})

    predictions = output() # 2d list for multiple images preditions
    images_with_predictions = [{'image': image, 'predictions': pred} for image, pred in zip(images, predictions)]

    return render(request, 'view_images.html', {'images_with_predictions': images_with_predictions, 'MEDIA_URL': settings.MEDIA_URL}) 