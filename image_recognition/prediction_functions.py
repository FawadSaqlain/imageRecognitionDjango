import tensorflow as tf  # loading the model and preprocessing the images

# Load the pre-trained MobileNetV2 model with ImageNet weights
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Global lists to store image paths and predictions
img_paths = []
predictions = []

def input_img(img_path):
    """
    Loads and preprocesses an image for model prediction.

    Args:
    img_path (str): Path to the image file.

    Returns:
    tuple: (PIL.Image object, preprocessed image array)
    """
    # Load image and resize to model input size
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
    # Convert image to array and preprocess for MobileNetV2
    input_image = tf.keras.preprocessing.image.img_to_array(img)
    input_image = tf.keras.applications.mobilenet_v2.preprocess_input(input_image)
    # Add batch dimension
    input_image = tf.expand_dims(input_image, axis=0)
    return img, input_image

def get_prediction(input_image):
    """
    Gets the prediction for the preprocessed image.

    Args:
    input_image (numpy.ndarray): Preprocessed image array.

    Returns:
    list: List of predicted classes and probabilities.
    """
    predictions = model.predict(input_image)
    # Decode the predictions to human-readable labels
    predicted_classes = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=10)[0]
    return predicted_classes

def printing_predictions(img, predicted_classes):
    """
    Formats predictions into a readable string.

    Args:
    img (PIL.Image object): The image.
    predicted_classes (list): List of tuples (class_id, class_name, probability).

    Returns:
    list: List of formatted prediction strings.
    """
    each_prediction = []
    for _, class_name, probability in predicted_classes:
        each_prediction.append(f"{class_name}: {probability:.4f}")
    return each_prediction

def output():
    """
    Processes all images in img_paths and generates predictions.

    Returns:
    list: List of lists containing predictions for each image.
    """
    predictions.clear()
    for image_path in img_paths:
        img, input_image = input_img(image_path)
        predicted_classes = get_prediction(input_image)
        predictions.append(printing_predictions(img, predicted_classes))
    return predictions
