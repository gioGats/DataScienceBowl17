import tflearn


def fully_connected(input_shape, layers, optimizer='adam', loss='categorical_crossentropy'):
    """
    Make a fully-connected neural network based on the input parameters
    :param input_shape: a list that when added to [None] describes the tensor dimensions of input data
    :param layers: a list where each entry describes a layer as a list of
            [number_of_nodes, probability_of_dropout, activation_function]
    :param optimizer: str of optimizer to use
    :param loss: str of loss function to use
    :return: a tflearn.DNN object
    """
    tflearn.init_graph()
    net = tflearn.input_data(shape=[None] + input_shape)
    for l in layers:
        num_nodes = l[0]
        dropout = l[1]
        activation_function = l[2]
        net = tflearn.fully_connected(net, num_nodes, activiation=activation_function)
        if dropout != 0:
            net = tflearn.dropout(net, dropout)
    net = tflearn.regression(net, optimizer=optimizer, loss=loss)
    return tflearn.DNN(net)
