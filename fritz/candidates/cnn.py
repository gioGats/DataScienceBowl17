import tflearn


def fully_connected(input_shape, layers, optimizer, loss):
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