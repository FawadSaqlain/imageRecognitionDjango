import tensorflow as tf #loading the model and preprocessing the images
import matplotlib.pyplot as plt #displaying the images and predictions.
model = tf.keras.applications.MobileNetV2(weights='imagenet')
img_paths = ['photos/car.jpeg','photos/bed.jpeg','photos/pen.jpeg','photos/umbrella.jpeg','photos/cat.jpeg','photos/dog.jpeg','photos/horse.jpeg','photos/elephant.jpeg']

def input_img(img_path):
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224,224))
    input_image = tf.keras.preprocessing.image.img_to_array(img)
    input_image = tf.keras.applications.mobilenet_v2.preprocess_input(input_image)
    input_image = tf.expand_dims(input_image, axis=0)
    return img,input_image

def get_prediction(input_image):
    predictions = model.predict(input_image)
    predicted_classes = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=10)[0]
    return predicted_classes

def printing_preditions(img,predicted_classes):
    plt.imshow(img,interpolation='bicubic')
    plt.axis('off')
    plt.show()
    print("Predictions:")
    first_prediction = True
    for _, class_name, probability in predicted_classes:
        if first_prediction:
            print(f"{class_name}: {probability}")
            first_prediction = False
        else:
            print(f"{class_name}: {probability}")
    print()

for image_path in img_paths:
    img,input_image =input_img(image_path)

    predicted_classes=get_prediction(input_image)

    printing_preditions(img,predicted_classes)