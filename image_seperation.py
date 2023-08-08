import tensorflow as tf
import tensorflow_hub as hub
import cv2

# Load the MobileNet V2 model from TensorFlow Hub
model_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/4"
model = hub.load(model_url)

# Load the image
image_path = r'F:\VS Code\Python\EduHelpBot\cat_dog.jpg'
image = cv2.imread(image_path)

# Check if the image was loaded successfully
if image is None:
    raise ValueError(f"Failed to load image: {image_path}")

# Preprocess the image
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (224, 224))
image = image / 255.0  # Normalize pixel values to [0, 1]

# Expand dimensions to create a batch of size 1
image = tf.expand_dims(image, axis=0)

# Run the model to perform object classification
predictions = model(image)

# Get the class labels
imagenet_labels_url = "https://tfhub.dev/google/imagenet/20190404/labels/1000.txt"
labels = tf.keras.utils.get_file('ImageNetLabels.txt', imagenet_labels_url)
with open(labels) as f:
    class_labels = f.readlines()
class_labels = [label.strip() for label in class_labels]

# Get the top predicted class
predicted_class_index = tf.argmax(predictions, axis=1).numpy()[0]
predicted_class_label = class_labels[predicted_class_index]

# Print the predicted class
print(f"Predicted class: {predicted_class_label}")
