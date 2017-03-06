from __future__ import division, print_function, absolute_import
import tflearn
from tflearn.layers.core import input_data, dropout, flatten
from tflearn.layers.estimator import regression


def network_in_network_2d(input_tensor, output_dimension=1, recurrent_layer='rnn', recurrent_params=None):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: 4D Tensor of input dimensions [batch, x, y, color_channels]
    :param output_dimension: Dimensions of output
    :param recurrent_layer: str of recurrent layer to use ['', 'rnn', 'lstm', 'gru']
    :param recurrent_params: dict of parameters for recurrent layer; see rnn directory for detail
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d

    network = input_data(shape=input_tensor)
    network = conv_2d(network, 192, 5, activation='relu')
    network = conv_2d(network, 160, 1, activation='relu')
    network = conv_2d(network, 96, 1, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = dropout(network, 0.5)
    network = conv_2d(network, 192, 5, activation='relu')
    network = conv_2d(network, 192, 1, activation='relu')
    network = conv_2d(network, 192, 1, activation='relu')
    network = avg_pool_2d(network, 3, strides=2)
    network = dropout(network, 0.5)
    network = conv_2d(network, 192, 3, activation='relu')
    network = conv_2d(network, 192, 1, activation='relu')

    # Last layer
    network = conv_2d(network, output_dimension, 1, activation='relu')
    # TODO Insert recurrence
    network = avg_pool_2d(network, 8)
    network = flatten(network)
    network = regression(network, optimizer='adam',
                         loss='softmax_categorical_crossentropy',
                         learning_rate=0.001)
    return tflearn.DNN(network)


def network_in_network_3d(input_tensor, output_dimension=1):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: 5D Tensor of input dimensions [batch, x, y, slices, color_channels]
    :param output_dimension: Dimensions of output
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    from tflearn.layers.conv import conv_3d, max_pool_3d, avg_pool_3d

    network = input_data(shape=input_tensor)
    network = conv_3d(network, 192, 5, activation='relu')
    network = conv_3d(network, 160, 1, activation='relu')
    network = conv_3d(network, 96, 1, activation='relu')
    network = max_pool_3d(network, 3, strides=2)
    network = dropout(network, 0.5)
    network = conv_3d(network, 192, 5, activation='relu')
    network = conv_3d(network, 192, 1, activation='relu')
    network = conv_3d(network, 192, 1, activation='relu')
    network = avg_pool_3d(network, 3, strides=2)
    network = dropout(network, 0.5)
    network = conv_3d(network, 192, 3, activation='relu')
    network = conv_3d(network, 192, 1, activation='relu')

    # Last layer
    network = conv_3d(network, output_dimension, 1, activation='relu')

    network = avg_pool_3d(network, 8)
    network = flatten(network)
    network = regression(network, optimizer='adam',
                         loss='softmax_categorical_crossentropy',
                         learning_rate=0.001)
    return tflearn.DNN(network)
