import tflearn


def alexnet_model_2d(input_tensor, output_dimension=1, recurrent_layer='rnn', recurrent_params=None):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: 5D Tensor of input dimensions [batch, x, y, color_channels]
    :param output_dimension: Dimensions of output
    :param recurrent_layer: str of recurrent layer to use ['', 'rnn', 'lstm', 'gru']
    :param recurrent_params: dict of parameters for recurrent layer; see rnn directory for detail
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    network = input_data(shape=input_tensor)
    network = conv_2d(network, 96, 11, strides=4, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_2d(network, 256, 5, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_2d(network, 384, 3, activation='relu')
    network = conv_2d(network, 384, 3, activation='relu')
    network = conv_2d(network, 256, 3, activation='relu')
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)

    # =====================================
    # Begin rnn layer insertion
    # =====================================
    if recurrent_layer == 'rnn':
        from ..rnn.simple_rnn import simple_rnn as recurrent_layer_function
    elif recurrent_layer == 'lstm':
        from ..rnn.lstm import lstm_layer as recurrent_layer_function
    elif recurrent_layer == 'gru':
        from ..rnn.gru import gru_layer as recurrent_layer_function
    elif recurrent_layer == '':
        def recurrent_layer_function(network, param_dict):
            return network
    else:
        raise NotImplementedError('Invalid recurrent layer type')

    network = recurrent_layer_function(network, recurrent_params)
    # =====================================
    # End rnn layer insertion
    # =====================================

    network = fully_connected(network, output_dimension, activation='softmax')
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=0.001)
    return tflearn.DNN(network, checkpoint_path='model_alexnet',
                    max_checkpoints=1, tensorboard_verbose=2)


def alexnet_model_3d(input_tensor, output_dimension=1):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: 5D Tensor of input dimensions [batch, x, y, slices, color_channels]
    :param output_dimension: Dimensions of output
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    network = input_data(shape=input_tensor)
    network = conv_3d(network, 96, 11, strides=4, activation='relu')
    network = max_pool_3d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_3d(network, 256, 5, activation='relu')
    network = max_pool_3d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = conv_3d(network, 384, 3, activation='relu')
    network = conv_3d(network, 384, 3, activation='relu')
    network = conv_3d(network, 256, 3, activation='relu')
    network = max_pool_3d(network, 3, strides=2)
    network = local_response_normalization(network)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, 4096, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, output_dimension, activation='softmax')
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=0.001)
    return tflearn.DNN(network, checkpoint_path='model_alexnet',
                    max_checkpoints=1, tensorboard_verbose=2)
