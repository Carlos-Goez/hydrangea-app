import numpy as np
import tensorflow as tf
from keras_preprocessing.image import load_img, img_to_array


class ClusterFlower:
    height, length = 200, 200
    model = 'converted_model.tflite'

    @staticmethod
    def predict(file):
        x = load_img(file, target_size=(ClusterFlower.length, ClusterFlower.height))
        x = img_to_array(x)
        x = np.expand_dims(x, axis=0)

        # Load TFLite model and allocate tensors.
        interpreter = tf.lite.Interpreter(model_path=ClusterFlower.model)
        interpreter.allocate_tensors()

        # Get input and output tensors.
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Test model on random input data.
        input_shape = input_details[0]['shape']
        input_data = np.array(x)
        interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = interpreter.get_tensor(output_details[0]['index'])
        dict_cluster = {'blue': output_data[0][0], 'mini': output_data[0][1], 'select': output_data[0][2]}
        return dict_cluster


print(ClusterFlower.predict('Fotos_Prueba/m1.jpg'))
