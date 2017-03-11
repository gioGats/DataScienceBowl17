import numpy as np
from skimage.transform import resize
from data_manipulation_1 import load_scan

"""
=================================================================================
For this branch (modular_preprocess), I have arbitrarily selected skimage as the
image preprocessing library.  It has unbelievably worse time performance compared
to openCV (11s vs 770s).  But it has much superior documentation and supports 3D
resizing natively.  We should strongly consider an openCV model to speed this up.
=================================================================================
"""


def three_d_preprocess(dicom_directory,
                       x=512, y=512, slices=100,
                       mode=None, processing=''):
    # Validate input, passed directly to skimage.transform.resize()
    if (mode is not None) and \
            (mode not in ['constant', 'edge', 'symmetric', 'reflect', 'wrap']):
        raise NotImplementedError('%s not a valid resizing mode' % mode)

    # TODO Use str param for processing to specify more processing functions
    if processing == '' or 'hu':
        from data_manipulation_1 import get_pixels_hu as processing

    # Bring all dicoms in dicom_directory into memory, and
    # process raw data values into a 2D numpy array (z, (x, y, channel))
    # with pixel values adjusted with processing function (defined above)
    patient_array = processing(load_scan(dicom_directory))

    # TODO Get patient label
    # label = get_label(dicom_directory.split('/')[-1])
    label = 1

    # Apply 2D resizing
    if slices <= 0:
        patient_array = resize(patient_array, (x, y, len(patient_array)), mode=mode)
    # Apply 3D resizing
    else:
        patient_array = resize(patient_array, (x, y, slices), mode=mode)
    return np.array([patient_array, label])

if __name__ == '__main__':
    test_individual = '/nvme/stage1_data/sample_images/0a0c32c9e08cc2ea76a71649de56be6d'
    three_d_preprocess(test_individual, slices=-1)
