from .alexnet import alexnet_model_2d, alexnet_model_3d
from .highway_conv import highway_model_2d, highway_model_3d
from .inception_resnet_v2 import inception_resnet_v2_2d, inception_resnet_v2_3d
from .inception_v3 import inception_v3_2d, inception_v3_3d
from .inception_v4 import inception_v4_2d, inception_v4_3d
from .net_in_net import network_in_network_2d, network_in_network_3d

import tflearn
import numpy
import pickle

if __name__ == '__main__':
    DEFAULT_input_2dtensor = [None, 100, 100, 3]  # TODO Arbitrary
    DEFAULT_input_3dtensor = [None, 100, 100, 25, 3]  # TODO Arbitrary
    DEFAULT_output_dimension = 1

    with open('/raw/trial_2d.np', 'rb') as f:  # TODO Pickle an example
        trial_2d = pickle.load(f)
        assert(isinstance(trial_2d, numpy.array))
        f.close()

    for model_2d in [alexnet_model_2d(DEFAULT_input_2dtensor, DEFAULT_output_dimension),
                     highway_model_2d(DEFAULT_input_2dtensor, DEFAULT_output_dimension),
                     inception_resnet_v2_2d(DEFAULT_input_2dtensor, DEFAULT_output_dimension),
                     inception_v3_2d(DEFAULT_input_2dtensor, DEFAULT_output_dimension),
                     inception_v4_2d(DEFAULT_input_2dtensor, DEFAULT_output_dimension),
                     network_in_network_2d(DEFAULT_input_2dtensor, DEFAULT_output_dimension)]:
        try:
            assert(isinstance(model_2d, tflearn.DNN))  # TODO Verify in tflearn docs
            prediction = model_2d.predict(trial_2d)
            # TODO Validate prediction is as specified in default_output_tensor
        except NotImplementedError:
            print("%s not implemented" % str(model_2d))

    with open('/raw/trial_3d.np', 'rb') as f:  # TODO Pickle an example
        trial_3d = pickle.load(f)
        assert(isinstance(trial_3d, numpy.array))
        f.close()

    for model_3d in [alexnet_model_3d(DEFAULT_input_3dtensor, DEFAULT_output_dimension),
                     highway_model_3d(DEFAULT_input_3dtensor, DEFAULT_output_dimension),
                     inception_resnet_v2_3d(DEFAULT_input_3dtensor, DEFAULT_output_dimension),
                     inception_v3_3d(DEFAULT_input_3dtensor, DEFAULT_output_dimension),
                     inception_v4_3d(DEFAULT_input_3dtensor, DEFAULT_output_dimension),
                     network_in_network_3d(DEFAULT_input_3dtensor, DEFAULT_output_dimension)]:
        try:
            assert(isinstance(model_3d, tflearn.DNN))  # TODO Verify in tflearn docs
            prediction = model_3d.predict(trial_3d)
            # TODO Validate prediction is as specified in default_output_tensor
        except NotImplementedError:
            print("%s not implemented" % str(model_3d))
