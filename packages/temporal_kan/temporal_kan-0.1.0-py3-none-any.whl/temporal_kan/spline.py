import tensorflow as tf

def power_spline(exponent):
    def activation(x):
        return tf.pow(x, exponent)
    return activation