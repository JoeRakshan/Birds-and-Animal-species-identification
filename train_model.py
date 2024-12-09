from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

# Set paths for training and validation data
train_directory = r"B:/animal and bird/static/Image/train"
test_directory = r"B:/animal and bird/static/Image/test"
IMAGE_SIZE = [224, 224]  # Define image size

# Load VGG16 model with pre-trained weights
vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# Freeze the layers of VGG16
for layer in vgg.layers:
    layer.trainable = False

# Prepare training data
ff = r"B:/animal and bird/static/Image/train/*"
folders = glob(ff)
num_classes = len(folders)

# Create model layers
x = Flatten()(vgg.output)
prediction = Dense(num_classes, activation='softmax')(x)

# Create model object
model = Model(inputs=vgg.input, outputs=prediction)

# View the structure of the model
model.summary()

# Compile the model
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Define ImageDataGenerator for training and testing
train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

# Create generators for training and testing
training_set = train_datagen.flow_from_directory(train_directory,
                                                 target_size=IMAGE_SIZE,
                                                 batch_size=32,
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory(test_directory,
                                            target_size=IMAGE_SIZE,
                                            batch_size=32,
                                            class_mode='categorical')

# Calculate steps per epoch
steps_per_epoch = len(training_set)
validation_steps = len(test_set)

# Train the model
r = model.fit(
    training_set,
    validation_data=test_set,
    epochs=20,
    steps_per_epoch=steps_per_epoch,
    validation_steps=validation_steps
)

# Plot training and validation loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()

# Plot training and validation accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()

# Save the model
model.save('animal_birds.h5')

# Load the model for prediction
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model1 = load_model('./animal_birds.h5', compile=False)

# Create a dictionary for class labels
lab = training_set.class_indices
lab = {k: v for v, k in lab.items()}
print(lab)

# Define a function for making predictions
def output(location):
    img = load_img(location, target_size=(224, 224))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, axis=0)
    answer = model1.predict(img)
    y_class = answer.argmax(axis=-1)
    res = lab[y_class[0]]  # Get the predicted class
    return res

# Example usage
img = 'B:/animal and bird/static/Image/train\American Crow/American_Crow_0020_25618.jpg'
pic = load_img(img, target_size=(224, 224))
plt.imshow(pic)
prediction_result = output(img)
print(f'Predicted class: {prediction_result}')
