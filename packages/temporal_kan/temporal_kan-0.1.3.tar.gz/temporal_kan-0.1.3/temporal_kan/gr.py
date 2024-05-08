from typing import List
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense
from tensorflow.keras import regularizers
from temporal_kan import power_spline


class GRKAN(Layer):
    def __init__(self, activation_funcs: List[str | int], num_outputs: int, return_sequences: bool = False, recurrent_dropout : float = 0.0, recurrent_activation = 'linear',
                 kernel_regularizer=None, recurrent_regularizer=None, bias_regularizer=None, **kwargs):
        super(GRKAN, self).__init__(**kwargs)
        self.activation_funcs = activation_funcs
        self.num_outputs = num_outputs
        self.recurrent_activation = tf.keras.activations.get(recurrent_activation)
        self.return_sequences = return_sequences
        self.recurrent_dropout = recurrent_dropout
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.recurrent_regularizer = regularizers.get(recurrent_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.sub_layers = [Dense(1, activation=power_spline(act) if isinstance(act, (int, float)) else act,
                                 kernel_regularizer=self.kernel_regularizer,
                                 bias_regularizer=self.bias_regularizer)
                           for act in activation_funcs]

        # Recurrent kernels for each sub-layer
        self.sub_recurrent_kernels = [self.add_weight(shape=(1, 1), initializer='uniform', trainable=True, regularizer=self.kernel_regularizer) for _ in activation_funcs]
        # Global recurrent kernel
        self.recurrent_kernel = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='uniform', trainable=True, regularizer=self.kernel_regularizer)

    def build(self, input_shape):
        # Aggregation weights
        self.aggregation_weights = self.add_weight(shape=(len(self.sub_layers), self.num_outputs), initializer='uniform', trainable=True, regularizer=self.kernel_regularizer, )

    def call(self, inputs, training=None):
        batch_size = tf.shape(inputs)[0]
        state = tf.zeros((batch_size, self.num_outputs))

        sub_states = [tf.zeros((batch_size, 1)) for _ in self.sub_layers]
        outputs = []

        # Initialize dropout mask once per batch
        dropout_mask = tf.ones((1, 1))
        global_dropout_mask = tf.ones((self.num_outputs, self.num_outputs))
        if training and self.recurrent_dropout > 0:
            dropout_mask = tf.nn.dropout(dropout_mask, rate=self.recurrent_dropout)
            global_dropout_mask = 1 - self.recurrent_dropout + tf.random.uniform((self.num_outputs, self.num_outputs)) * self.recurrent_dropout

        for t in range(inputs.shape[1]):
            current_input = inputs[:, t, :]
            layer_outputs = []
            new_sub_states = []

            for idx, (sub_layer, sub_state, rec_kernel) in enumerate(zip(self.sub_layers, sub_states, self.sub_recurrent_kernels)):
                sub_output = sub_layer(current_input) + tf.linalg.matmul(sub_state, rec_kernel * dropout_mask)
                sub_output = self.recurrent_activation(sub_output)
                new_sub_states.append(sub_output)
                layer_outputs.append(sub_output)

            sub_states = new_sub_states
            concatenated_outputs = tf.concat(layer_outputs, axis=-1)

            # Global state update

            state = tf.linalg.matmul(concatenated_outputs, self.aggregation_weights) + tf.linalg.matmul(state, self.recurrent_kernel * global_dropout_mask)
            state = self.recurrent_activation(state)

            if self.return_sequences:
                outputs.append(state)

        return tf.stack(outputs, axis=1) if self.return_sequences else state
