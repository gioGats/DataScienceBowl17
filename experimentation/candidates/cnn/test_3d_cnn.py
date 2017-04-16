from alexnet import alexnet_model_3d
from highway_conv import highway_model_3d
from inception_resnet_v2 import inception_resnet_v2_3d
from inception_v3 import inception_v3_3d
from inception_v4 import inception_v4_3d
from net_in_net import network_in_network_3d

import tflearn
import h5py
import numpy as np
import pickle
import traceback
import sys

if __name__ == '__main__':
    hdf5 = h5py.File('raw/3D_(100,100,20)_constant_hu_DEBUG.hdf5', 'r')
    try:
        num_subsets = int((len(hdf5) - 1) / 2)

        train_subset_indicies = range(0, num_subsets-2)
        train_subsets = []
        for i in train_subset_indicies:
            train_subsets.append([hdf5['subset_%d_X' % i], hdf5['subset_%d_Y' % i]])

        validation_subset_index = num_subsets - 2
        X_validation = hdf5['subset_%d_X' % validation_subset_index]
        Y_validation = hdf5['subset_%d_Y' % validation_subset_index]

        test_subset_index = num_subsets - 1
        X_test = hdf5['subset_%d_X' % test_subset_index]
        Y_test = hdf5['subset_%d_Y' % test_subset_index]

        input_shape = X_test.shape[1:]
        input_tensor = [None] + list(input_shape)
        output_shape = 1

        print(input_tensor, output_shape)

        for model_generator in [alexnet_model_3d, highway_model_3d, inception_resnet_v2_3d,
                                inception_v3_3d, inception_v4_3d, network_in_network_3d]:
            print(model_generator.__name__)
            try:
                clf = model_generator(input_tensor, output_shape)
                assert(isinstance(clf, tflearn.DNN))
                raise RuntimeError  # FUTURE Remove and test full functionality (probably need GPU)
                """
                for subset in train_subsets:
                    clf.fit(subset[0], subset[1], n_epoch=1, validation_set=(X_validation, Y_validation))

                print(clf.predict(X_test))
                """
            except NotImplementedError:
                print("%s not implemented" % str(clf))
            except RuntimeError:  # FUTURE Remove and test full functionality (probably need GPU)
                print("%s created succesfully" % model_generator.__name__)
            except Exception:
                traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
                raise RuntimeError
    except RuntimeError:
        pass
    except Exception:
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    hdf5.close()
