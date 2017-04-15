import sys
import os
import subprocess
import pandas as pd


def get_label(patient_id, data_dir):
    labels_df = pd.read_csv(data_dir, index_col=0)
    l = labels_df.get_value(patient_id, 'cancer')
    return l


if __name__ == '__main__':
    try:
        tld = sys.argv[1]
        truth = sys.argv[2]
    except IndexError:
        print('USAGE: python3 label_dirs tld_path truth_path')
    for dir in os.listdir(tld):
        subprocess.run(['mv', '%s/%s' % (tld, dir), '%s/%s_%s' % (tld, dir, get_label(dir, truth))])