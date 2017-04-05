from .three_d import three_d_preprocess as preprocess
import numpy as np
import h5py
import os
import math


def name_dataset(preprocess_params):
    shape = preprocess_params['shape']
    mode = preprocess_params['mode']
    processing = preprocess_params['processing']
    mirroring = preprocess_params['mirroring']
    blurring = preprocess_params['blurring']

    if shape[2] <= 0:
        return_string = '2D_(%d,%d)_%s_%s' % (shape[0], shape[1], mode, processing)
    else:
        return_string = '3D_(%d,%d,%d)_%s_%s' % (shape[0], shape[1], shape[2], mode, processing)
    if mirroring:
        return_string += '-M'
    if blurring:
        return_string += '-B'
    return return_string + '.hdf5'


def generate_subset_indicies(num_subsets, num_examples):
    subset_indicies = []
    for i in range(num_subsets):
        start = math.ceil(num_examples*(i/10))
        if num_examples % num_subsets == 0:
            stop = int(num_examples*((i+1)/10) - 1)
        else:
            stop = math.floor(num_examples*((i+1)/10))
        subset_indicies.append((start, stop))
    return subset_indicies


def make_preprocess_function(general_function, preprocess_params):
    x = preprocess_params['x']
    y = preprocess_params['y']

    # TODO Return a specific preprocess function that takes only the dicom_directory as input

    return x


def make_dataset(data_directory, target_directory, preprocess_params,
                 exs_per_patient=16, num_subsets=10, flush_freq=100, debug=False):
    if debug:
        data_directory += '/sample_images'
    else:
        data_directory += '/all_images'

    f = h5py.File(target_directory + '/' + name_dataset(preprocess_params))
    patient_ids = np.array(os.listdir(data_directory), dtype='<U34')
    np.random.shuffle(patient_ids)

    subset_indicies = generate_subset_indicies(num_subsets, len(patient_ids))
    for subset in subset_indicies:
        examples_in_subset = subset[1] - subset[0] + 1
        dset = f.create_dataset('subset_%d' % subset_indicies.index(subset),
                                (examples_in_subset*exs_per_patient, SOMETHING),
                                dtype='uint16', chunks=True)  # TODO VERIFY ARRAY SHAPE
        for i in range(subset[1] - subset[0] + 1):
            patient_id = patient_ids[i + subset[0]]
            preprocess_fn = make_preprocess_function(preprocess, preprocess_params)
            values = preprocess_fn(patient_id)
            for j in len(values):
                dset[i + j*examples_in_subset] = values[j]
            if i % flush_freq == 0:
                f.flush()

    dset = f.create_dataset('patient_ids', data=patient_ids, chunks=True)
    f.flush()
    f.close()

if __name__ == '__main__':
    print(generate_subset_indicies(10, 109000))
    usr_data_dir = '/storage/nstc/raw_data'
    usr_tgt_dir = '/storage/nstc/candiate_datasets'

    # TODO Record metadata
    # TODO Preprocess function lambda
    # TODO Port unit testing from old file
