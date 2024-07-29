from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect
import os
from .prediction_functions import img_paths, output

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
        # Save the image file
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Add the image path to session
        if 'img_paths' not in request.session:
            request.session['img_paths'] = []
        request.session['img_paths'].append(file_path)
        request.session.modified = True

        # Optional redirect after upload
        return redirect('view_images')
    
    return render(request, 'htmlFiles/upload.html')

def view_images(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # Retrieve image paths from session
    if 'img_paths' not in request.session:
        request.session['img_paths'] = []
    image_paths = request.session['img_paths']

    images = []
    for image_path in image_paths:
        title = os.path.basename(image_path)  # Use filename as title
        images.append({'title': title, 'filename': os.path.basename(image_path)})

    # Print paths for debugging
    for image in images:
        full_path = os.path.join(settings.MEDIA_ROOT, 'images', image['filename'])
        print(f"Processing image: {full_path}")
        if not os.path.exists(full_path):
            print(f"Error: File not found at {full_path}")

    # Ensure img_paths in prediction_functions matches the session img_paths
    img_paths.clear()
    img_paths.extend(image_paths)

    predictions = output()  # Get predictions for all images
    if len(predictions) != len(images):
        raise ValueError("The number of predictions does not match the number of images")
    
    images_with_predictions = [{'image': image, 'predictions': pred} for image, pred in zip(images, predictions)]

    return render(request, 'htmlFiles/view_images.html', {'images_with_predictions': images_with_predictions, 'MEDIA_URL': settings.MEDIA_URL})

def clear_session(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    # Clear session data
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
    # Clear the image paths from session
    if 'img_paths' in request.session:
        del request.session['img_paths']
    
    logout(request)
    return HttpResponseRedirect(reverse("login"))
