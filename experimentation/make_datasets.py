from .candidates.preprocess.make_dataset import make_dataset
import numpy as np
import h5py

if __name__ == '__main__':
    stage1_data = '/nvme/stage1_data/stage1'
    stage1_sample = '/nvme/stage1_data/sample_images'
    datasets_to_create = []
    for dim_2d in [100, 200, 300, 400]:
        for slices in [-1, 20, 50, 100]:
            for mode in ['constant', 'edge', 'symmetric', 'reflect', 'wrap']:
                for mirroring in [None, ['lr', 'ud', 'fb']]:
                    make_dataset(stage1_sample, x=dim_2d, y=dim_2d,
                                 slices=slices, mode=mode, mirroring_axes=mirroring, chunk_size=-1)
                    # TODO start ds upload to GDrive
