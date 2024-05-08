"""Standard KAN layer, not used otherwhere in the project.

Simple example implementation for tensorflow of a KAN layer

"""

import tensorflow as tf
from tensorflow.keras.layers import Layer
from temporal_kan import power_spline

class KAN(Layer):
    def __init__(self, activation_funcs, num_outputs, **kwargs):
        super(KAN, self).__init__(**kwargs)
        self.activation_funcs = activation_funcs  # List of activation functions
        self.num_outputs = num_outputs  # Number of outputs from the layer
        self.sub_layers = [tf.keras.layers.Dense(1, activation=power_spline(act) if isinstance(act, (int, float)) else act, trainable=True) for act in activation_funcs]
        self.aggregation_weights = self.add_weight(
            shape=(len(self.sub_layers), self.num_outputs),
            initializer='uniform',
            trainable=True
        )

    def build(self, input_shape):
        for layer in self.sub_layers:
            layer.build(input_shape)


    def call(self, inputs):
        layer_outputs = [sub_layer(inputs) for sub_layer in self.sub_layers]
        concatenated_outputs = tf.concat(layer_outputs, axis=-1)
        final_output = tf.linalg.matmul(concatenated_outputs, self.aggregation_weights)
        return final_output