import tflearn


def highway_model_2d(input_tensor=[None, 100, 100], output_tensor=[None, 1]):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: Dimensions of input
    :param output_tensor: Dimensions of output
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    raise NotImplementedError


def highway_model_3d(input_tensor=[None, 100, 100, 25], output_tensor=[None, 1]):
    """
    Generates an inception model that conforms to specified input/output tensors.
    :param input_tensor: Dimensions of input
    :param output_tensor: Dimensions of output
    :return: An instance of tflearn.DNN class supporting {fit, predict, evaluate, save, load} methods
    """
    # TODO Can this even be done?
    raise NotImplementedError