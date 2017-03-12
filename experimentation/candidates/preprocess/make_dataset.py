from .three_d import three_d_preprocess
from .two_d import two_d_preprocess
import numpy as np
import h5py
import os
import pickle

"""
=================================================================================
For this branch (modular_preprocess), I have yet to implement full h5py
functionality.  Eventually, it looks like we will need a chunk-oriented save
operation.  This is not an issue initally with sample images, but will cause
problems in the larger datasets.
=================================================================================
"""


def make_dataset(top_directory, x=512, y=512, slices=100, mode=None,
                 processing='', mirroring_axes=None, chunk_size=10):
    """
    Applys function parameters to make an h5py dataset of all patients in top_directory.
    :param top_directory: path to directory with patient directories
    :param x: x dimension of output
    :param y: y dimension of output
    :param slices: number of slices in output
    :param mode: One of 'constant', 'edge', 'symmetric', 'reflect', 'wrap'
    :param processing: 'hu'
    :param mirroring_axes: 0 or more of ['lr', 'ud', 'fb']
    :param chunk_size:
    """
    chunk_array = np.array([])
    i = 0
    total = len(os.listdir(top_directory))
    h5f = h5py.File(name_dataset(x=x, y=y, slices=slices, mode=mode,
                                 processing=processing, mirroring_axes=mirroring_axes), 'w')

    for patient_dir in os.listdir(top_directory):
        if slices < 0:
            processed_patient = two_d_preprocess(patient_dir, x=x, y=y, mode=mode,
                                                 processing=processing, mirroring_axes=mirroring_axes)
        else:
            processed_patient = three_d_preprocess(patient_dir, x=x, y=y, slices=slices, mode=mode,
                                                   processing=processing, mirroring_axes=mirroring_axes)
        i += 1
        if chunk_size == -1:
            chunk_array = array_merge(chunk_array, processed_patient)
        elif i % chunk_size == 0:
            # TODO Save dataset_array to h5f
            chunk_array = np.array([])
        else:
            chunk_array = array_merge(chunk_array, processed_patient)

        # Report progress
        print('\rProgress: .2f' % ((i/total)*100))

    if chunk_size == -1:
        name = name_dataset(x=x, y=y, slices=slices, mode=mode, processing=processing, mirroring_axes=mirroring_axes)
        name = name[:-2] + 'np'
        with open(name, 'wb') as f:
            pickle.dump(chunk_array, f)
            f.close()


def array_merge(dataset_array, new_example_array):
    # TODO Verify correct axis preserved in merge
    return np.concatenate((dataset_array, new_example_array))


def name_dataset(x, y, slices, mode, processing, mirroring_axes):
    if slices <= 0:
        dim = '2D'
    else:
        dim = '3D'
    if mode is None:
        mode = 'constant'  # default
    if processing == '':
        processing = 'hu'  # default
    if mirroring_axes is None:
        mirroring_axes = ''  # default
    return '%s_%dx%dx%d_%s_%s_%s.h5' % (dim, x, y, slices, mode, processing, mirroring_axes)


if __name__ == '__main__':
    # Testing
    make_dataset('/nvme/stage1_data/sample_images', chunk_size=-1)
