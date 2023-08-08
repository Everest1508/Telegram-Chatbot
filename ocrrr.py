import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
from tensorflow.keras import layers

# Load the EMNIST dataset
emnist_ds = tfds.load("emnist", split="train", shuffle_files=True)

# Split the dataset into training and testing
emnist_train, emnist_test = emnist_ds["train"], emnist_ds["test"]

# Convert the dataset to numpy arrays
x_train, y_train = tfds.as_numpy(emnist_train)
x_test, y_test = tfds.as_numpy(emnist_test)

# Preprocess the data
x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

# Modify the number of classes to 26 for the entire alphabet
num_classes = 26

# Define the model architecture
model = keras.Sequential(
    [
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation="softmax"),
    ]
)

# Compile the model
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model
model.fit(x_train, y_train, batch_size=128, epochs=15, validation_split=0.1)

# Evaluate the model
_, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy:", test_acc)

# Save the model
model.save("handwritten_text_model_alphabets.h5")
