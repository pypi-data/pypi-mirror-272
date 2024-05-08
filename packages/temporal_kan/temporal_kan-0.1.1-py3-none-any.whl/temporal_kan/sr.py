from typing import List
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense
from tensorflow.keras import regularizers
from temporal_kan import power_spline


class SRKAN(Layer):
    def __init__(self, activation_funcs: List[str | int], num_outputs: int, return_sequences: bool = False, recurrent_dropout : float = 0.0, recurrent_activation = 'linear',
                 kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, **kwargs):
        super(SRKAN, self).__init__(**kwargs)
        self.activation_funcs = activation_funcs
        self.num_outputs = num_outputs
        self.return_sequences = return_sequences
        self.recurrent_dropout = recurrent_dropout
        self.recurrent_activation = tf.keras.activations.get(recurrent_activation)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.recurrent_regularizer = regularizers.get(recurrent_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)

        # Initialize sub_layers with regularizers
        self.sub_layers = [Dense(1, activation=power_spline(act) if isinstance(act, (int, float)) else act,
                                 kernel_regularizer=self.kernel_regularizer,
                                 bias_regularizer=self.bias_regularizer)
                           for act in activation_funcs]

    def build(self, input_shape):
        # Aggregation weights that combine outputs from each sub-layer
        self.aggregation_weights = self.add_weight(
            shape=(len(self.sub_layers), self.num_outputs),
            initializer='uniform',
            trainable=True,
            regularizer=self.kernel_regularizer,  # Applying kernel regularizer to aggregation weights
            name='aggregation_weights'
        )

        # Recurrent kernel that processes the aggregated output
        self.recurrent_kernel = self.add_weight(
            shape=(self.num_outputs, self.num_outputs),
            initializer='uniform',
            trainable=True,
            regularizer=self.recurrent_regularizer,  # Applying recurrent regularizer to recurrent kernel
            name='recurrent_kernel'
        )

        super(SRKAN, self).build(input_shape)  # Ensure the base class is aware that the layer is built

    def call(self, inputs, training=None):
        batch_size = tf.shape(inputs)[0]
        state = tf.zeros((batch_size, self.num_outputs))
        outputs = []

        # Initialize dropout mask once per batch
        dropout_mask = tf.ones((self.num_outputs, self.num_outputs))
        if training and self.recurrent_dropout > 0:
            dropout_mask = tf.nn.dropout(dropout_mask, rate=self.recurrent_dropout)


        for t in range(inputs.shape[1]):
            current_input = inputs[:, t, :]
            layer_outputs = [sub_layer(current_input) for sub_layer in self.sub_layers]
            concatenated_outputs = tf.concat(layer_outputs, axis=-1)
            state = self.recurrent_activation(state)
            # Update state with weighted sum of current activations and previous state
            state = tf.linalg.matmul(concatenated_outputs, self.aggregation_weights) + tf.linalg.matmul(state, self.recurrent_kernel * dropout_mask)

            if self.return_sequences:
                outputs.append(state)


        return tf.stack(outputs, axis=1) if self.return_sequences else state

