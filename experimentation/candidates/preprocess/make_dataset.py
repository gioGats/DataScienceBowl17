from .three_d import three_d_preprocess
from .two_d import two_d_preprocess
import numpy as np
import os


def make_dataset(top_directory,
                    x=512, y=512, slices=100, channels=1,
                    upsample='', downsample='', processing=''):
    dataset_array = np.array([])
    for patient_dir in os.listdir(top_directory):
        if slices < 0:
            processed_patient = two_d_preprocess(patient_dir,
                                                 x=x, y=y, channels=channels,
                                                 upsample=upsample, downsample=downsample,
                                                 processing=processing)
        else:
            processed_patient = three_d_preprocess(patient_dir,
                                                   x=x, y=y, slices=slices, channels=channels,
                                                   upsample=upsample, downsample=downsample,
                                                   processing=processing)
        dataset_array = array_merge(dataset_array, processed_patient)

    return dataset_array


def array_merge(dataset_array, new_example_array):
    # TODO Merge the arrays while preserving axises
    return []

if __name__ == '__main__':
    # Testing
    ds = make_dataset('/nvme/stage1_data/sample_images')