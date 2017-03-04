import tflearn


def highway_model_2d(input_tensor, output_dimension=1, recurrent_layer='rnn', recurrent_params=None):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: 5D Tensor of input dimensions [batch, x, y, color_channels]
    :param output_dimension: Dimensions of output
    :param recurrent_layer: str of recurrent layer to use ['', 'rnn', 'lstm', 'gru']
    :param recurrent_params: dict of parameters for recurrent layer; see rnn directory for detail
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    network = input_data(shape=input_tensor, name='input')
    #highway convolutions with pooling and dropout
    for i in range(3):
        for j in [3, 2, 1]:
            network = highway_conv_2d(network, 16, j, activation='elu')
        network = max_pool_2d(network, 2)
        network = batch_normalization(network)

    network = fully_connected(network, 128, activation='elu')
    network = fully_connected(network, 256, activation='elu')

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
    network = regression(network, optimizer='adam', learning_rate=0.01,
                         loss='categorical_crossentropy', name='target')

    return tflearn.DNN(network, tensorboard_verbose=0)


def highway_model_3d(input_tensor, output_dimension=1):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: 5D Tensor of input dimensions [batch, x, y, slices, color_channels]
    :param output_dimension: Dimensions of output
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    network = input_data(shape=input_tensor, name='input')
    #highway convolutions with pooling and dropout
    for i in range(3):
        for j in [3, 2, 1]:
            network = highway_conv_3d(network, 16, j, activation='elu')
        network = max_pool_3d(network, 2)
        network = batch_normalization(network)

    network = fully_connected(network, 128, activation='elu')
    network = fully_connected(network, 256, activation='elu')
    network = fully_connected(network, output_dimension, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=0.01,
                         loss='categorical_crossentropy', name='target')

    # Training
    return tflearn.DNN(network, tensorboard_verbose=0)