from alexnet import alexnet_model_3d
from inception_resnet_v2 import inception_resnet_v2_3d
from inception_v3 import inception_v3_3d
from net_in_net import network_in_network_3d

import tflearn
import h5py
import traceback
import sys
import os

DATA_DIR = '/storage/data/processed_datasets'


def increment_filename(filename, path=''):
    if path != '' and path[-1] != '/':
        path += '/'
    if not os.path.exists(path + filename):
        return path + filename
    else:
        if not filename.split('.')[-2][-2] == '_':
            return path + filename.split('.')[0] + '_0.' + filename.split('.')[1]
        else:
            num_index = filename.index('_') + 1
            new_filelist = list(filename)
            new_filelist[num_index] = str(int(new_filelist[num_index]) + 1)
            new_filename = ''.join(new_filelist)
            return path + new_filename


def model_creation(test_run):
    hdf5 = h5py.File('raw/3D_(100,100,20)_constant_hu_DEBUG.hdf5', 'r')
    # noinspection PyBroadException
    # | Used to ensure hdf5 file is always closed to limit corruption risk
    try:
        num_subsets = int((len(hdf5) - 1) / 2)

        train_subset_indicies = range(0, num_subsets-2)
        train_subsets = []
        for i in train_subset_indicies:
            train_subsets.append([hdf5['subset_%d_X' % i], hdf5['subset_%d_Y' % i]])

        validation_subset_index = num_subsets - 2
        x_validation = hdf5['subset_%d_X' % validation_subset_index]
        y_validation = hdf5['subset_%d_Y' % validation_subset_index]

        test_subset_index = num_subsets - 1
        x_test = hdf5['subset_%d_X' % test_subset_index]
        y_test = hdf5['subset_%d_Y' % test_subset_index]

        input_shape = x_test.shape[1:]
        input_tensor = [None] + list(input_shape)
        output_shape = 1

        print(input_tensor, output_shape)

        for model_generator in [alexnet_model_3d, network_in_network_3d,
                                inception_resnet_v2_3d, inception_v3_3d]:
            print(model_generator.__name__, end='')
            try:
                clf = model_generator(input_tensor, output_shape)
                assert(isinstance(clf, tflearn.DNN))
                print(' | created successfully | ', end='')

                if not test_run:
                    print('test run skipped')
                else:
                    for subset in train_subsets:
                       clf.fit(subset[0], subset[1], n_epoch=1, validation_set=(x_validation, y_validation))
                    print(clf.predict(x_test))
            except NotImplementedError:
                print("%s not implemented" % str(model_generator.__name__))
            except Exception:
                traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    except Exception:
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    hdf5.close()


def test_size(hdf5_file, model_generator):
    hdf5 = h5py.File(hdf5_file, 'r')
    # noinspection PyBroadException
    # | Used to ensure hdf5 file is always closed to limit corruption risk
    try:
        num_subsets = int((len(hdf5) - 1) / 2)

        train_subset_indicies = range(0, num_subsets-2)
        train_subsets = []
        for i in train_subset_indicies:
            train_subsets.append([hdf5['subset_%d_X' % i], hdf5['subset_%d_Y' % i]])

        validation_subset_index = num_subsets - 2
        x_validation = hdf5['subset_%d_X' % validation_subset_index]
        y_validation = hdf5['subset_%d_Y' % validation_subset_index]

        test_subset_index = num_subsets - 1
        x_test = hdf5['subset_%d_X' % test_subset_index]
        y_test = hdf5['subset_%d_Y' % test_subset_index]

        input_shape = x_test.shape[1:]
        input_tensor = [None] + list(input_shape)
        output_shape = 1

        try:
            clf = model_generator(input_tensor, output_shape)
            assert(isinstance(clf, tflearn.DNN))
            for subset in train_subsets:
               clf.fit(subset[0], subset[1], n_epoch=100, validation_set=(x_validation, y_validation))
            print(clf.predict(x_test))
        except NotImplementedError:
            print("%s not implemented" % str(model_generator.__name__))
        except Exception:
            traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    except Exception:
        traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    hdf5.close()


if __name__ == '__main__':
    if '-mc' in sys.argv:
        # Beware of running -tr (test run) without GPU support
        model_creation(('-tr' in sys.argv))

    if '-st' in sys.argv:
        # Beware of running -st (size test) without GPU support
        for mg in [alexnet_model_3d, network_in_network_3d]:
            for filename in sorted(os.listdir(DATA_DIR)):
                if 'DEBUG' not in filename:
                    continue
                if '(50,50,50)' not in filename:
                    continue
                print(filename)
                full_filename = DATA_DIR + '/' + filename
                test_size(full_filename, mg)




