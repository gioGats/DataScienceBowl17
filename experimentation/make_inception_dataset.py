import numpy as np
import tflearn
import sys
import os
import h5py


class RealInception(object):
    def __init__(self, output_d):
        raise NotImplementedError

    def predict(self, x):
        raise NotImplementedError


class TestInception(object):
    def __init__(self, output_d):
        assert(isinstance(output_d, int))
        self.output_dimension = output_d

    def predict(self, x):
        return np.random.random((self.output_dimension, 1)).astype(np.float32)


def process_hdf5(clf, hdf5_name, data_dir, inception_return_length):
    #assert(isinstance(clf, tflearn.DNN))
    src = h5py.File(data_dir + '/processed_datasets/' + hdf5_name)
    tgt = h5py.File(data_dir + '/inception_data/' + hdf5_name, 'w')

    # Copy Y
    tgt.create_dataset('Y', data=src['Y'][:])

    # Select X groups
    src_x_grp = src['X']
    tgt_x_grp = tgt.create_group('X')

    for patient_id in src_x_grp:
        tgt_dset = tgt_x_grp.create_dataset(
            patient_id,
            shape=(len(src_x_grp[patient_id]), inception_return_length, 1),
            dtype=np.float32)
        for slice_name in src_x_grp[patient_id]:
            slice_index = int(slice_name)
            slice_dset = src_x_grp[patient_id][slice_name]
            val = clf.predict(slice_dset[:])
            tgt_dset[slice_index] = val


if __name__ == '__main__':
    data_directory = '/storage/data'
    if '-debug' in sys.argv:
        test_clf = TestInception(2047)
        for file_name in os.listdir(data_directory + '/processed_datasets'):
            if 'DEBUG' in file_name and '2D' in file_name:
                process_hdf5(test_clf, file_name, data_directory, test_clf.output_dimension)

    elif '-all' in sys.argv and '2D' in sys.argv:
        test_clf = RealInception(2047)
        for file_name in os.listdir(data_directory + '/processed_datasets'):
            if 'DEBUG' not in file_name and '2D' in file_name:
                process_hdf5(test_clf, file_name, data_directory, test_clf.output_dimension)
