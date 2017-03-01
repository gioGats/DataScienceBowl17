from __future__ import division, print_function, absolute_import


def network_in_network_2d(input_tensor, output_dimension):
    import tflearn
    from tflearn.layers.core import input_data, dropout, flatten
    from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
    from tflearn.layers.estimator import regression

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

    network = avg_pool_2d(network, 8)
    network = flatten(network)
    network = regression(network, optimizer='adam',
                         loss='softmax_categorical_crossentropy',
                         learning_rate=0.001)
    return tflearn.DNN(network)


def network_in_network_3d(input_tensor, output_dimension):
    import tflearn
    from tflearn.layers.core import input_data, dropout, flatten
    from tflearn.layers.conv import conv_3d, max_pool_3d, avg_pool_3d
    from tflearn.layers.estimator import regression

    # TODO Continue refactoring here
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

    network = avg_pool_2d(network, 8)
    network = flatten(network)
    network = regression(network, optimizer='adam',
                         loss='softmax_categorical_crossentropy',
                         learning_rate=0.001)
    raise NotImplementedError
    return tflearn.DNN(network)
