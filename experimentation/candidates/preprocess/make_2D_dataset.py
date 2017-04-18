from .three_d import load_scan, get_pixels_hu
from .make_3D_dataset import name_dataset
from skimage.transform import resize
import numpy as np
import h5py
import os


def make_2d_dataset(data_directory, preprocess_params, debug=False):
    target_directory = data_directory + '/processed_datasets/'
    if debug:
        data_directory += '/sample_images'
    else:
        data_directory += '/all_images'

    patient_id_list = sorted(os.listdir(data_directory))

    f = h5py.File(target_directory + name_dataset(preprocess_params, debug))
    labels_dset = f.create_dataset('Y', (len(patient_id_list), 1), dtype=np.int8)
    x_group = f.require_group('X')

    for i in range(len(patient_id_list)):
        print('\rProgress: %d of %d' % (i, len(patient_id_list)), end='')
        patient_id = patient_id_list[i]

        patient_group = x_group.require_group(patient_id)

        patient_array = load_scan(data_directory + '/' + patient_id)

        if preprocess_params['process'] == '' or preprocess_params['process'] == 'hu':
            # adjust pixel values  with processing function
            patient_array = get_pixels_hu(patient_array)
        else:
            raise NotImplementedError('%s not a valid processing mode' % processing)

        labels_dset[i][0] = int(patient_id[-1])

        for j in range(len(patient_array)):
            slice_array = resize(patient_array[j],
                                 (preprocess_params['x'], preprocess_params['y']),
                                 mode=preprocess_params['mode'])
            patient_group.create_dataset(str(j), data=slice_array, dtype=np.int16)







