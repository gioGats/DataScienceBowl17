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
                       mode=None, processing='', mirroring_axes=None):
    """

    :param dicom_directory:
    :param x:
    :param y:
    :param slices:
    :param mode:
    :param processing:
    :param mirroring_axes:
    :return:
    """
    # Validate input, passed directly to skimage.transform.resize()
    if (mode is not None) and \
            (mode not in ['constant', 'edge', 'symmetric', 'reflect', 'wrap']):
        raise NotImplementedError('%s not a valid resizing mode' % mode)

    # TODO Use str param for processing to specify more processing functions
    if processing == '' or 'hu':
        from data_manipulation_1 import get_pixels_hu as processing

    # Bring all dicoms in dicom_directory into memory
    # with pixel values adjusted with processing function (defined above)
    patient_array = processing(load_scan(dicom_directory))

    patient_id = dicom_directory.split('/')[-1]
    label = get_label(patient_id)

    # Apply 2D resizing
    if slices <= 0:
        patient_array = resize(patient_array, (x, y, len(patient_array)), mode=mode)
    # Apply 3D resizing
    else:
        patient_array = resize(patient_array, (x, y, slices), mode=mode)

    # Apply mirroring
    return_arrays = [patient_array, label]
    if mirroring_axes is not None:
        if 'lr' in mirroring_axes:  # mirror x axis
            return_arrays.append([np.flip(patient_array, 1), label])
        if 'ud' in mirroring_axes:  # mirror y axis
            return_arrays.append([np.flip(patient_array, 2), label])
        if 'fb' in mirroring_axes and slices >= 0:  # mirror z axis
            return_arrays.append([np.flip(patient_array, 0), label])
    return np.array(return_arrays)


def get_label(patient_id, data_dir='/nvme/stage1_data/'):
    labels_df = pd.read_csv(data_dir + 'stage1_labels.csv', index_col=0)
    label = labels_df.get_value(patient_id, 'cancer')
    return label


if __name__ == '__main__':
    test_individual = '/nvme/stage1_data/sample_images/0a0c32c9e08cc2ea76a71649de56be6d'
    three_d_preprocess(test_individual, slices=-1)
