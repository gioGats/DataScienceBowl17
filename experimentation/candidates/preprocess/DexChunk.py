"""
3dDex - SentDex: 3D Adaptation
"""


def DexChunk(abspath, dim_px=50, dim_slice=20):
    
    import dicom 
    import os 
    import pandas as pd
    import cv2
    import numpy as np
    import math
    import h5py
    import sys
    
    data_dir = abspath
    patients = os.listdir(data_dir)
    labels_df = pd.read_csv(abspath+'stage1_labels.csv', index_col=0)
    
    def chunks(l, n):
        # Credit: Ned Batchelder
        # Link: http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def mean(a):
        return sum(a) / len(a)

    def process_data(patient, labels_df, img_px_size=50, hm_slices=20):
        label = labels_df.get_value(patient, 'cancer')
        path = data_dir + patient
        slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
        slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))

        new_slices = []
        slices = [cv2.resize(np.array(each_slice.pixel_array),(dim_px,dim_px)) for each_slice in slices]
        
        chunk_sizes = math.ceil(len(slices) / hm_slices)
        for slice_chunk in chunks(slices, chunk_sizes):
            slice_chunk = list(map(mean, zip(*slice_chunk)))
            new_slices.append(slice_chunk)

        while len(new_slices) != hm_slices:
            if len(new_slices) < hm_slices:
                new_slices.append(new_slices[-1])
            else:
                new_val = list(map(mean, zip(*[new_slices[hm_slices-1],new_slices[hm_slices],])))
                del new_slices[hm_slices]
                new_slices[hm_slices-1] = new_val

        h5f = h5py.File('data.h5', 'a')
            
        if label == 1:
            label_p=np.array([0,1])
            h5f.create_dataset('positive', data=label_p)
            label = h5f['positive'][:]
        elif label == 0:
            label_n=np.array([1,0])
            h5f.create_dataset('negative', data=label_n)
            label = h5f['negative'][:]

        numpy_slices = np.array(new_slices)
        h5f.create_dataset(patient, data=numpy_slices)
        h5_slices = h5f[patient][:]

        
        h5f.close()

        return h5_slices,label
 
    D_proc = []

    for patient in enumerate(patients):
        img_data,label = process_data(patient,labels_df,dim_px,dim_slice)
        D_proc.append([img_data,label])

    return None


DexChunk()
