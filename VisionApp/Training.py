import sys
import os
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.python.keras.layers import Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as k

k.clear_session()

data_training = './data/Training/'
data_validation = './data/Validation'

numbers_epoch = 20
height, length = 200, 200
batch_size = 1
steps = 17
steps_validation = 40
filters_conv1 = 32
filters_conv2 = 64
size_filter1 = (3, 3)
size_filter2 = (2, 2)
size_pool = (2, 2)
number_class = 3
learning_rate = 0.0001

# Pre processing images

training_data_generator = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=True
)

validation_data_generator = ImageDataGenerator(
    rescale=1. / 255
)

images_training = training_data_generator.flow_from_directory(
    data_training,
    target_size=(height, length),
    batch_size=batch_size,
    class_mode='categorical'
)

images_validation = validation_data_generator.flow_from_directory(
    data_validation,
    target_size=(height, length),
    batch_size=batch_size,
    class_mode='categorical')

# Create Neuronal Network

cnn = Sequential()
cnn.add(Convolution2D(filters_conv1,
                      size_filter1,
                      padding='same',
                      input_shape=(height, length, 3),
                      activation='relu'
                      )
        )

cnn.add(MaxPooling2D(pool_size=size_pool))

cnn.add(Convolution2D(filters_conv2,
                      size_filter2,
                      padding='same',
                      activation='relu'
                      )
        )

cnn.add(MaxPooling2D(pool_size=size_pool))

cnn.add(Flatten())
cnn.add(Dense(256, activation='relu'))
cnn.add(Dropout(0.5))
cnn.add(Dense(number_class, activation='softmax'))

cnn.compile(loss='categorical_crossentropy',
            optimizer=optimizers.Adam(lr=learning_rate),
            metrics=['accuracy']
            )
cnn.fit(images_training,
        steps_per_epoch=steps,
        epochs=numbers_epoch,
        validation_data=images_validation,
        validation_steps=steps_validation
        )

directory = './model'

if not os.path.exists(directory):
    os.mkdir(directory)

cnn.save('./model/model.h5')
cnn.save_weights('./model/pesos.h5')
