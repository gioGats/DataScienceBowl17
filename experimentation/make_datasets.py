#!/usr/bin/env Python3

from candidates.preprocess.make_dataset import make_dataset
import itertools
import sys
from joblib import Parallel, delayed

#  Note: GDrive upload size limit is 5.2TB
DATA_PATH = '/storage/data'
DEBUG = False


def all_combinations(vary_dim2d=True, vary_slices=True,
                     vary_mode=True, vary_processing=True,
                     vary_mirroring=True, vary_blurring=True):
    if vary_dim2d:
        combinations = [[100, 200, 300, 400]]
    else:
        combinations = [[50, 100]]
    if vary_slices:
        combinations.append([20, 50, 100])
    else:
        combinations.append([-1])
    if vary_mode:
        combinations.append(['constant', 'edge', 'symmetric', 'reflect', 'wrap'])
    else:
        combinations.append(['constant'])
    if vary_processing:
        combinations.append(['hu'])
    else:
        combinations.append(['hu'])
    if vary_mirroring:
        combinations.append([True, False])
    else:
        combinations.append([False])
    if vary_blurring:
        combinations.append([True, False])
    else:
        combinations.append([False])
    return itertools.product(*combinations)


def make_param_dict(full_tuple):
    return {'x': full_tuple[0],
            'y': full_tuple[0],
            'z': full_tuple[1],
            'mode': full_tuple[2],
            'process': full_tuple[3],
            'mirror': full_tuple[4],
            'blur': full_tuple[5]}


def exs_per_patient(full_tuple):
    # HARDCODED PARAMS
    mirror_multiple = 8
    blur_multiple = 2

    total = 1
    if full_tuple[4]:
        total *= mirror_multiple
    if full_tuple[5]:
        total += blur_multiple
    return total


def make_dataset_wrapper(full_tuple, num_subsets=10, flush_freq=100):
    make_dataset(data_directory=DATA_PATH,
                 preprocess_params=make_param_dict(full_tuple),
                 exs_per_patient=exs_per_patient(full_tuple),
                 num_subsets=num_subsets,
                 flush_freq=flush_freq,
                 debug=DEBUG)


if __name__ == '__main__':
    if '-debug' in sys.argv:
        params_iter = all_combinations(vary_dim2d=False, vary_slices=False,
                                       vary_mode=False, vary_processing=False,
                                       vary_mirroring=False, vary_blurring=False)

        Parallel(n_jobs=-1, verbose=3)(delayed(make_dataset_wrapper)(i) for i in params_iter)
    elif '-size' in sys.argv:
        params_iter = all_combinations(vary_dim2d=True, vary_slices=True,
                                       vary_mode=False, vary_processing=False,
                                       vary_mirroring=False, vary_blurring=False)

        Parallel(n_jobs=-1, verbose=3)(delayed(make_dataset_wrapper)(i) for i in params_iter)
    elif '-all' in sys.argv:
        params_iter = all_combinations(vary_dim2d=False, vary_slices=False,
                                       vary_mode=True, vary_processing=True,
                                       vary_mirroring=True, vary_blurring=True)

        Parallel(n_jobs=-1, verbose=3)(delayed(make_dataset_wrapper)(i) for i in params_iter)
    else:
        print('USAGE STATEMENT')
