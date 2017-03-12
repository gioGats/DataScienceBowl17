import numpy as np
from skimage.transform import resize

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
    Processes a directory of dicom files into a numpy array. (3D)
    :param dicom_directory: path to directory with dicom files
    :param x: x dimension of output
    :param y: y dimension of output
    :param slices: number of slices in output
    :param mode: One of 'constant', 'edge', 'symmetric', 'reflect', 'wrap'
    :param processing: 'hu'
    :param mirroring_axes: 0 or more of ['lr', 'ud', 'fb']
    :return: np.array of [[slices, x, y], label]
    """
    # Validate input, passed directly to skimage.transform.resize()
    if (mode is not None) and \
            (mode not in ['constant', 'edge', 'symmetric', 'reflect', 'wrap']):
        raise NotImplementedError('%s not a valid resizing mode' % mode)

    # Bring all dicoms in dicom_directory into memory
    patient_array = load_scan(dicom_directory)

    # TODO Use str param for processing to specify more processing functions
    # Look to kaggle tutorials for inspiration

    if processing == '' or 'hu':
        # adjust pixel values  with processing function
        patient_array = get_pixels_hu(patient_array)

    patient_id = dicom_directory.split('/')[-1]
    label = get_label(patient_id)

    # TODO Speed up the resizing/mirroring code (multi-thread or gpu)
    # Look into opencv/other libraries

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
    # TODO May want to abstract this to a higher level;
    # passing a labels file as input, instead of loading the labels file for every patient.
    labels_df = pd.read_csv(data_dir + 'stage1_labels.csv', index_col=0)
    label = labels_df.get_value(patient_id, 'cancer')
    return label


def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    # noinspection PyBroadException
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except Exception as e:
        print(e)
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices


def get_pixels_hu(slices):
    image = np.stack([s.pixel_array for s in slices])
    image = image.astype(np.int16)
    image[image == -2000] = 0
    for slice_number in range(len(slices)):
        intercept = slices[slice_number].RescaleIntercept
        slope = slices[slice_number].RescaleSlope

        if slope != 1:
            image[slice_number] = slope * image[slice_number].astype(np.float64)
            image[slice_number] = image[slice_number].astype(np.int16)

        image[slice_number] += np.int16(intercept)

    return np.array(image, dtype=np.int16)


if __name__ == '__main__':
    test_individual = '/nvme/stage1_data/sample_images/0a0c32c9e08cc2ea76a71649de56be6d'
    three_d_preprocess(test_individual, slices=-1)
