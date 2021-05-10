import numpy as np
from keras_preprocessing.image import load_img, img_to_array
from keras.models import load_model

height, length = 200, 200

model = './model/model.h5'
#weight = './model/pesos.h5'
cnn = load_model(model)
#cnn.load_weights(weight)


def predict(file):
    x = load_img(file, target_size=(length, height))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    array = cnn.predict(x)
    result = array[0]
    respond = np.argmax(result)
    if respond == 0:
        print('blue')
    if respond == 1:
        print('mini')
    if respond == 2:
        print('select')
    return respond


print(predict('Fotos_Prueba/b2.jpg'))
