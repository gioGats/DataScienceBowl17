import numpy as np
import tflearn
import sys
import os
import h5py


class TestInception(object):
    def __init__(self, output_d):
        assert(isinstance(output_d, int))
        self.output_dimension = output_d

    def predict(self, x):
        return np.ones((self.output_dimension, 1), dtype=np.float32)


def process_hdf5(clf, hdf5_name, data_dir, inception_return_length):
    assert(isinstance(clf, tflearn.DNN))
    processed_directory = data_dir + '/all_images/'
    inception_directory = data_dir + '/inception_data/'
    src = h5py.File(processed_directory + hdf5_name)
    tgt = h5py.File(inception_directory + hdf5_name)

    # Copy Y
    tgt.create_dataset('Y', data=src['Y'][:])

    # Select X groups
    src_x_grp = src['X']
    tgt_x_grp = tgt.create_group('X')

    for patient_id in src_x_grp:
        tgt_dset = tgt_x_grp.create_dataset(
            patient_id,
            shape=(len(src_x_grp), inception_return_length),
            dtype=np.float32)
        for slice_name in src_x_grp[patient_id]:
            slice_index = int(slice_name)  # TODO It might be slice_name - 1
            tgt_dset[slice_index] = clf.predict(rc_x_grp[patient_id][slice_name][:])


if __name__ == '__main__':
    data_directory = '/storage/data'
    test_clf = TestInception(1000)
    if '-debug' in sys.argv:
        for file_name in os.listdir(data_directory + '/all_images'):
            if 'DEBUG' in file_name:
                process_hdf5(test_clf, file_name, data_directory, test_clf.output_dimension)

    elif '-all' in sys.argv:
        for file_name in os.listdir(data_directory + '/all_images'):
            if 'DEBUG' not in file_name:
                process_hdf5(test_clf, file_name, data_directory, test_clf.output_dimension)
