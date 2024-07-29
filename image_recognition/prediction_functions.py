###########################################################################################
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import tensorflow as tf  # loading the model and preprocessing the images

model = tf.keras.applications.MobileNetV2(weights='imagenet')

img_paths = []
predictions = []

def input_img(img_path):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224, 224))
    input_image = tf.keras.preprocessing.image.img_to_array(img)
    input_image = tf.keras.applications.mobilenet_v2.preprocess_input(input_image)
    input_image = tf.expand_dims(input_image, axis=0)
    return img, input_image

def get_prediction(input_image):
    predictions = model.predict(input_image)
    predicted_classes = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=10)[0]
    return predicted_classes

def printing_predictions(img, predicted_classes):
    each_prediction = []
    for _, class_name, probability in predicted_classes:
        each_prediction.append(f"{class_name}: {probability:.4f}")
    return each_prediction

def output():
    predictions.clear()
    for image_path in img_paths:
        img, input_image = input_img(image_path)
        predicted_classes = get_prediction(input_image)
        predictions.append(printing_predictions(img, predicted_classes))
    return predictions
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
###########################################################################################