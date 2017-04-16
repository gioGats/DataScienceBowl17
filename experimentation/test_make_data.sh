#!/usr/bin/env bash

find /storage -name '.DS_Store' -type f -delete

find /storage/data/processed_datasets -name *hdf5 -type f -delete

python3 experimentation/make_datasets.py -debug