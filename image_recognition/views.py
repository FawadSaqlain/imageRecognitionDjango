from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
import os
from .prediction_functions import img_paths , output

# Function to clear file contents
def clear_file(file_path):
    """
    Clears the contents of the file at the given path.
    
    Args:
    file_path (str): The path to the file to be cleared.
    """
    try:
        with open(file_path, 'w') as file:
            # Opening in write mode ('w') will truncate the file to zero length
            pass
        print(f"File '{file_path}' has been cleared.")
    except Exception as e:
        print(f"An error occurred while clearing the file: {e}")

def upload_image(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
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

        # Write the image details to images.txt
        with open(os.path.join(images_dir, 'images.txt'), 'a') as file:
            file.write(f"{title},{uploaded_file.name}\n")

        # Optional redirect after upload
        return redirect('view_images')
    
    return render(request, 'htmlFiles/upload.html')

def view_images(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    images = []
    images_file_path = os.path.join(settings.MEDIA_ROOT, 'images', 'images.txt')

    if os.path.exists(images_file_path):
        with open(images_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                title, filename = line.strip().split(',')
                images.append({'title': title, 'filename': filename})

    # Print paths for debugging
    for image in images:
        full_path = os.path.join(settings.MEDIA_ROOT, 'images', image['filename'])
        print(f"Processing image: {full_path}")
        if not os.path.exists(full_path):
            print(f"Error: File not found at {full_path}")

    predictions = output()  # 2d list for multiple images predictions
    images_with_predictions = [{'image': image, 'predictions': pred} for image, pred in zip(images, predictions)]

    return render(request, 'htmlFiles/view_images.html', {'images_with_predictions': images_with_predictions, 'MEDIA_URL': settings.MEDIA_URL})

def clear_session(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    request.session.flush()
    return redirect('login')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("upload_image"))
        else:
            return render(request, "htmlFiles/login.html", {
                "message": "Invalid credentials.",
                "username": username  # Retain the entered username
            })
    return render(request, "htmlFiles/login.html")

def logout_view(request):
    # Clear the image.txt file
    images_file_path = os.path.join(settings.MEDIA_ROOT, 'images', 'images.txt')
    clear_file(images_file_path)
    
    logout(request)
    return HttpResponseRedirect(reverse("login"))
