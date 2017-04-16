#!/usr/bin/env bash

# Makes datasets of sample data for testing gpu memory growth of cnn networks.

echo "DEPRECATION WARNING: This file not updated for 2APR refactor"

cd /nvme/DataScienceBowl17/experimentation
echo '500 250'
python3 make_datasets.py 500 250 /raid/dsb_data
python3 make_datasets.py 500 -1 /raid/dsb_data

echo '300 150'
python3 make_datasets.py 300 150 /raid/dsb_data
python3 make_datasets.py 300 -1 /raid/dsb_data

echo '200 100'
python3 make_datasets.py 200 100 /raid/dsb_data
python3 make_datasets.py 200 -1 /raid/dsb_data

echo '100 50'
python3 make_datasets.py 100 50 /raid/dsb_data
python3 make_datasets.py 100 -1 /raid/dsb_data

echo '50 25'
python3 make_datasets.py 50 25 /raid/dsb_data
python3 make_datasets.py 50 -1 /raid/dsb_data
