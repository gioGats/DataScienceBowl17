#!/usr/bin/env Python3

from .three_d import three_d_preprocess as preprocess
import numpy as np
import h5py
import os
import math


def name_dataset(preprocess_params, debug=False):
    x = preprocess_params['x']
    y = preprocess_params['y']
    z = preprocess_params['z']
    mode = preprocess_params['mode']
    processing = preprocess_params['process']
    mirroring = preprocess_params['mirror']
    blurring = preprocess_params['blur']

    if z <= 0:
        return_string = '2D_(%d,%d)_%s_%s' % (x, y, mode, processing)
    else:
        return_string = '3D_(%d,%d,%d)_%s_%s' % (x, y, z, mode, processing)
    if mirroring:
        return_string += '-M'
    if blurring:
        return_string += '-B'
    if debug:
        return_string += '_DEBUG'
    return return_string + '.hdf5'


def generate_subset_indicies(num_subsets, num_examples):
    subset_indicies = []
    for i in range(num_subsets):
        start = math.ceil(num_examples*(i/num_subsets))
        if num_examples % num_subsets == 0:
            stop = int(num_examples*((i+1)/num_subsets) - 1)
        else:
            stop = math.floor(num_examples*((i+1)/num_subsets))
        if i == num_subsets - 1:
            subset_indicies.append((start, min(num_examples-1, stop)))
        else:
            subset_indicies.append((start, stop))
    return subset_indicies


def make_preprocess_function(general_function, preprocess_params):
    x = preprocess_params['x']
    y = preprocess_params['y']
    z = preprocess_params['z']
    mode = preprocess_params['mode']
    process = preprocess_params['process']
    mirror = preprocess_params['mirror']
    blur = preprocess_params['blur']
    return lambda pat_id: general_function(pat_id, x, y, z, mode, process, mirror, blur)


def get_shape(preprocess_params):
    return preprocess_params['x'], preprocess_params['y'], preprocess_params['z']


def record_metadata(file, preprocess_params):
    pass
    # FUTURE


def make_dataset(data_directory, preprocess_params,
                 exs_per_patient=16, num_subsets=10, flush_freq=100, debug=False):
    target_directory = data_directory + '/processed_datasets'
    if debug:
        data_directory += '/sample_images'
    else:
        data_directory += '/all_images'

    f = h5py.File(target_directory + '/' + name_dataset(preprocess_params, debug))
    patient_ids = np.array(os.listdir(data_directory), dtype='<U34')
    np.random.shuffle(patient_ids)

    subset_indicies = generate_subset_indicies(num_subsets, len(patient_ids))
    for subset in subset_indicies:
        examples_in_subset = subset[1] - subset[0] + 1
        dset_x = f.create_dataset('subset_%d_X' % subset_indicies.index(subset),
                                  ((examples_in_subset*exs_per_patient,) + get_shape(preprocess_params) + (1,)),
                                  dtype=np.int16, chunks=True)
        dset_y = f.create_dataset('subset_%d_Y' % subset_indicies.index(subset),
                                  (examples_in_subset*exs_per_patient,),
                                  dtype=np.int16, chunks=True)
        for i in range(subset[1] - subset[0] + 1):
            patient_id = patient_ids[i + subset[0]]
            preprocess_fn = make_preprocess_function(preprocess, preprocess_params)
            cubes, labels = preprocess_fn('%s/%s' % (data_directory, patient_id))
            for j in range(len(cubes)):
                dset_x[i + j*examples_in_subset] = cubes[j].reshape(cubes[j].shape + (1,))
                dset_y[i + j*examples_in_subset] = labels[j]
            if i % flush_freq == 0:
                f.flush()

    dset = f.create_dataset('patient_ids', data=patient_ids.astype('|S34'), dtype='S34', chunks=True)
    f.flush()
    record_metadata(f, preprocess_params)
    f.close()

if __name__ == '__main__':
    pass
    # FUTURE Port unit testing from old file
