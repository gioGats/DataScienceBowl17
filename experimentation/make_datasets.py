from candidates.preprocess.make_dataset import make_dataset
import numpy as np
import h5py
import sys

stage1_data = '/nvme/stage1_data/stage1'
stage1_sample = '/nvme/stage1_data/sample_images'

if __name__ == '__main__':
    if len(sys.argv) > 2:
        dim_2d = int(sys.argv[1])
        slices = int(sys.argv[2])
        # Additional params commented out for initial dataset creation
        # mode = sys.argv[4]
        # mirroring = sys.argv[5]
        # dest = sys.argv[6]
        dest = sys.argv[3]
        make_dataset(stage1_sample, x=dim_2d, y=dim_2d, slices=slices,
                     chunk_size=-1, dest=dest)

    if sys.argv[1] == '--loop':

        datasets_to_create = []
        for dim_2d in [100, 200, 300, 400]:
            for slices in [-1, 20, 50, 100]:
                for mode in ['constant', 'edge', 'symmetric', 'reflect', 'wrap']:
                    for mirroring in [None, ['lr', 'ud', 'fb']]:
                        make_dataset(stage1_sample, x=dim_2d, y=dim_2d,
                                     slices=slices, mode=mode, mirroring_axes=mirroring, chunk_size=-1)
                        # TODO start ds upload to GDrive
