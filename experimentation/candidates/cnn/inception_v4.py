import tflearn


def inception_v4_2d(input_tensor, output_dimension=1, recurrent_layer='rnn', recurrent_params=None):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: 4D Tensor of input dimensions [batch, x, y, color_channels]
    :param output_dimension: Dimensions of output
    :param recurrent_layer: str of recurrent layer to use ['', 'rnn', 'lstm', 'gru']
    :param recurrent_params: dict of parameters for recurrent layer; see rnn directory for detail
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    # SPRINT3 Implement tflearn wrapper around raw tensorflow
    raise NotImplementedError


def inception_v4_3d(input_tensor, output_dimension=1):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: 5D Tensor of input dimensions [batch, x, y, slices, color_channels]
    :param output_dimension: Dimensions of output
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    # SPRINT3 Implement tflearn wrapper around raw tensorflow
    raise NotImplementedError
