from typing import List
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense
from tensorflow.keras import regularizers
from temporal_kan import power_spline


class SLSTM_KAN(Layer):
    def __init__(self, activation_funcs: List[str | int], num_outputs: int, return_sequences: bool = False, recurrent_dropout : float = 0.0, **kwargs):
        super(SLSTM_KAN, self).__init__(**kwargs)
        self.activation_funcs = activation_funcs
        self.num_outputs = num_outputs
        self.return_sequences = return_sequences
        self.recurrent_dropout = recurrent_dropout
        self.sub_layers = [tf.keras.layers.Dense(1, activation=power_spline(act) if isinstance(act, (int, float)) else act) for act in activation_funcs]

        # LSTM gate weights
        self.Wi = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='glorot_uniform', trainable=True)
        self.Wf = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='glorot_uniform', trainable=True)
        self.Wo = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='glorot_uniform', trainable=True)
        self.Wc = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='glorot_uniform', trainable=True)

        self.Ui = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='orthogonal', trainable=True)
        self.Uf = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='orthogonal', trainable=True)
        self.Uo = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='orthogonal', trainable=True)
        self.Uc = self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='orthogonal', trainable=True)

        self.bi = self.add_weight(shape=(self.num_outputs,), initializer='zeros', trainable=True)
        self.bf = self.add_weight(shape=(self.num_outputs,), initializer='ones', trainable=True)  # Initialize forget gate bias to 1
        self.bo = self.add_weight(shape=(self.num_outputs,), initializer='zeros', trainable=True)
        self.bc = self.add_weight(shape=(self.num_outputs,), initializer='zeros', trainable=True)

    def build(self, input_shape):
        # Weights for aggregating outputs into the recurrent state
        self.aggregation_weights = self.add_weight(
            shape=(len(self.sub_layers), self.num_outputs),
            initializer='uniform',
            trainable=True
        )

    def call(self, inputs, training=None):
        batch_size = tf.shape(inputs)[0]
        hidden_state = tf.zeros((batch_size, self.num_outputs))
        cell_state = tf.zeros((batch_size, self.num_outputs))
        outputs = []

        for t in range(inputs.shape[1]):
            current_input = inputs[:, t, :]
            layer_outputs = [sub_layer(current_input) for sub_layer in self.sub_layers]

            concatenated_outputs = tf.linalg.matmul(tf.concat(layer_outputs, axis=-1), self.aggregation_weights)
            if training:
                dropout_mask = 1.0 - self.recurrent_dropout + tf.random.uniform((batch_size, self.num_outputs)) * self.recurrent_dropout
            else:
                dropout_mask = 1.0

            # LSTM Gates calculations
            xi = tf.nn.sigmoid(tf.linalg.matmul(concatenated_outputs, self.Wi) + tf.linalg.matmul(hidden_state * dropout_mask, self.Ui) + self.bi)
            xf = tf.nn.sigmoid(tf.linalg.matmul(concatenated_outputs, self.Wf) + tf.linalg.matmul(hidden_state * dropout_mask, self.Uf) + self.bf)
            xo = tf.nn.sigmoid(tf.linalg.matmul(concatenated_outputs, self.Wo) + tf.linalg.matmul(hidden_state * dropout_mask, self.Uo) + self.bo)
            xc = tf.nn.tanh(tf.linalg.matmul(concatenated_outputs, self.Wc) + tf.linalg.matmul(hidden_state * dropout_mask, self.Uc) + self.bc)

            # Update cell and hidden states
            cell_state = xf * cell_state + xi * xc
            hidden_state = xo * tf.nn.tanh(cell_state)

            if self.return_sequences:
                outputs.append(hidden_state)

        return tf.stack(outputs, axis=1) if self.return_sequences else hidden_state

