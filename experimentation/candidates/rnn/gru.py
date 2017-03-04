import tflearn


def gru_layer(network, param_dict=None):
    if param_dict is None:
        param_dict = {
            'n_units': 128,
            'activation': 'tanh',
            'inner_activation': 'sigmoid',
            'dropout': None,
            'bias': True,
            'weights_init': None,
            'return_seq': False,
            'return_state': False,
            'initial_state': None,
            'dynamic': False,
            'trainable': True,
            'restore': True,
            'reuse': False,
            'scope': None

        }
    return tflearn.lstm(network,
                        n_units=param_dict['n_units'],
                        activation=param_dict['activation'],
                        inner_activation=param_dict['inner_activation'],
                        dropout=param_dict['dropout'],
                        bias=param_dict['bias'],
                        weights_init=param_dict['weights_init'],
                        return_seq=param_dict['return_seq'],
                        return_state=param_dict['return_state'],
                        initial_state=param_dict['initial_state'],
                        dynamic=param_dict['dynamic'],
                        trainable=param_dict['trainable'],
                        restore=param_dict['restore'],
                        reuse=param_dict['reuse'],
                        scope=param_dict['scope'])