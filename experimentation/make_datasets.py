from .candidates.preprocess.make_dataset import make_dataset
import numpy as np
import h5py

if __name__ == '__main__':
    stage1_data = '/nvme/stage1_data/stage1'
    datasets_to_create = []
    # TODO Define a range of test datasets to create
    for dataset_params in datasets_to_create:
        # TODO Fill in make_dataset() params from dataset_params
        ds = make_dataset(stage1_data)
        # TODO save ds as h5py
        # TODO start ds upload to GDrive
