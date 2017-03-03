from .alexnet import alexnet_model_2d, alexnet_model_3d
from .highway_conv import highway_model_2d, highway_model_3d
from .inception_resnet_v2 import inception_resnet_v2_2d, inception_resnet_v2_3d
from .inception_v3 import inception_v3_2d, inception_v3_3d
from .inception_v4 import inception_v4_2d, inception_v4_3d
from .net_in_net import network_in_network_2d, network_in_network_3d

import tflearn
import numpy

if __name__ == '__main__':
    default_input_2dtensor = [None, 512, 512, 3]  # TODO Arbitrary
    default_input_3dtensor = [None, 512, 512, 25, 3]  # TODO Arbitrary
    default_output_tensor = [None, 1]
    trial_2d = numpy.array([[]])  # TODO Complete trial images
    trial_3d = numpy.array([[[]]])
    for model_2d in [alexnet_model_2d(default_input_2dtensor, default_output_tensor),
                     highway_model_2d(default_input_2dtensor, default_output_tensor),
                     inception_resnet_v2_2d(default_input_2dtensor, default_output_tensor),
                     inception_v3_2d(default_input_2dtensor, default_output_tensor),
                     inception_v4_2d(default_input_2dtensor, default_output_tensor),
                     network_in_network_2d(default_input_2dtensor, default_output_tensor)]:
        try:
            assert(isinstance(model_2d, tflearn.DNN))  # TODO Verify in tflearn docs
            prediction = model_2d.predict(trial_2d)
            # TODO Validate prediction is as specified in default_output_tensor
        except NotImplementedError:
            print("%s not implemented" % str(model_2d))

    for model_3d in [alexnet_model_3d(default_input_3dtensor, default_output_tensor),
                     highway_model_3d(default_input_3dtensor, default_output_tensor),
                     inception_resnet_v2_3d(default_input_3dtensor, default_output_tensor),
                     inception_v3_3d(default_input_3dtensor, default_output_tensor),
                     inception_v4_3d(default_input_3dtensor, default_output_tensor),
                     network_in_network_3d(default_input_3dtensor, default_output_tensor)]:
        try:
            assert(isinstance(model_3d, tflearn.DNN))  # TODO Verify in tflearn docs
            prediction = model_3d.predict(trial_3d)
            # TODO Validate prediction is as specified in default_output_tensor
        except NotImplementedError:
            print("%s not implemented" % str(model_3d))
