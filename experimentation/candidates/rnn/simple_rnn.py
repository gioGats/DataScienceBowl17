import tflearn


def simple_rnn(layers, dropout='', activation='', evaluation='', comp_vision=''):
    """

    :param layers: list of ints that specify number of nodes in each layer (len of layers is num layers)
    :param dropout: list of [0,1] floats that specifiy p_dropout applied to corresponding layer
    :param activation: any of the supported tflearn methods
    :param evaluation: any of the supported tflearn methods
    :param comp_vision: any of the models available from 'import cnn'
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    pass