from typing import List
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense
from tensorflow.keras import regularizers
from temporal_kan import power_spline



class GLSTM_KAN(Layer):
    def __init__(self, activation_funcs: List[str | int], num_outputs: int, return_sequences: bool = False, recurrent_dropout : float = 0.0, **kwargs):
        super(GLSTM_KAN, self).__init__(**kwargs)
        self.activation_funcs = activation_funcs
        self.num_outputs = num_outputs
        self.return_sequences = return_sequences
        self.recurrent_dropout = recurrent_dropout
        self.aggregation_transform = tf.keras.layers.Dense(num_outputs, activation=power_spline(act))


        # Sub-layer LSTM components
        self.sub_layers = []
        self.sub_lstm_gates = {'input': [], 'forget': [], 'output': [], 'cell': []}
        for act in activation_funcs:
            self.sub_layers.append(tf.keras.layers.Dense(1, activation=power_spline(act) if isinstance(act, (int, float)) else act))
            for gate in ['input', 'forget', 'output', 'cell']:
                self.sub_lstm_gates[gate].append(
                    self.add_weight(shape=(1, 1), initializer='glorot_uniform', trainable=True))

        # Global LSTM gate weights
        self.global_lstm_gates = {
            'Wi': self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='glorot_uniform', trainable=True),
            'Wf': self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='glorot_uniform', trainable=True),
            'Wo': self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='glorot_uniform', trainable=True),
            'Wc': self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='glorot_uniform', trainable=True)
        }

        self.global_recurrent_weights = {
            'Ui': self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='orthogonal', trainable=True),
            'Uf': self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='orthogonal', trainable=True),
            'Uo': self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='orthogonal', trainable=True),
            'Uc': self.add_weight(shape=(self.num_outputs, self.num_outputs), initializer='orthogonal', trainable=True)
        }

        self.global_biases = {
            'bi': self.add_weight(shape=(self.num_outputs,), initializer='zeros', trainable=True),
            'bf': self.add_weight(shape=(self.num_outputs,), initializer='ones', trainable=True),
            'bo': self.add_weight(shape=(self.num_outputs,), initializer='zeros', trainable=True),
            'bc': self.add_weight(shape=(self.num_outputs,), initializer='zeros', trainable=True)
        }

    def call(self, inputs, training=None):
        batch_size = tf.shape(inputs)[0]
        sub_hidden_states = [tf.zeros((batch_size, 1)) for _ in self.activation_funcs]
        sub_cell_states = [tf.zeros((batch_size, 1)) for _ in self.activation_funcs]
        global_hidden_state = tf.zeros((batch_size, self.num_outputs))
        global_cell_state = tf.zeros((batch_size, self.num_outputs))
        outputs = []

        for t in range(inputs.shape[1]):
            current_input = inputs[:, t, :]
            new_sub_hidden_states = []
            new_sub_cell_states = []
            sub_outputs = []

            for idx, sub_layer in enumerate(self.sub_layers):
                # Process each sub-layer independently with its own LSTM logic
                sub_input = sub_layer(current_input)
                sub_xi = tf.nn.sigmoid(sub_input * self.sub_lstm_gates['input'][idx])
                sub_xf = tf.nn.sigmoid(sub_input * self.sub_lstm_gates['forget'][idx])
                sub_xo = tf.nn.sigmoid(sub_input * self.sub_lstm_gates['output'][idx])
                sub_xc = tf.nn.tanh(sub_input * self.sub_lstm_gates['cell'][idx])

                sub_cell_state = sub_xf * sub_cell_states[idx] + sub_xi * sub_xc
                sub_hidden_state = sub_xo * tf.nn.tanh(sub_cell_state)
                new_sub_hidden_states.append(sub_hidden_state)
                new_sub_cell_states.append(sub_cell_state)
                sub_outputs.append(sub_hidden_state)

            # Global LSTM processing of aggregated sub-outputs
            aggregated_input = tf.concat(sub_outputs, axis=-1)
            # Transform aggregated input to match LSTM gate dimensions
            transformed_input = self.aggregation_transform(aggregated_input)

            # Apply dropout if training
            dropout_mask = 1 - self.recurrent_dropout + tf.random.uniform((batch_size, self.num_outputs)) * self.recurrent_dropout if training else 1.0

            # LSTM gate calculations...
            global_xi = tf.nn.sigmoid(tf.linalg.matmul(transformed_input, self.global_lstm_gates['Wi']) + tf.linalg.matmul(global_hidden_state * dropout_mask, self.global_recurrent_weights['Ui']) + self.global_biases['bi'])
            global_xf = tf.nn.sigmoid(tf.linalg.matmul(transformed_input, self.global_lstm_gates['Wf']) + tf.linalg.matmul(global_hidden_state * dropout_mask, self.global_recurrent_weights['Uf']) + self.global_biases['bf'])
            global_xo = tf.nn.sigmoid(tf.linalg.matmul(transformed_input, self.global_lstm_gates['Wo']) + tf.linalg.matmul(global_hidden_state * dropout_mask, self.global_recurrent_weights['Uo']) + self.global_biases['bo'])
            global_xc = tf.nn.tanh(tf.linalg.matmul(transformed_input, self.global_lstm_gates['Wc']) + tf.linalg.matmul(global_hidden_state * dropout_mask, self.global_recurrent_weights['Uc']) + self.global_biases['bc'])

            global_cell_state = global_xf * global_cell_state + global_xi * global_xc
            global_hidden_state = global_xo * tf.nn.tanh(global_cell_state)

            if self.return_sequences:
                outputs.append(global_hidden_state)

        return tf.stack(outputs, axis=1) if self.return_sequences else global_hidden_state

