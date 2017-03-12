

def two_d_preprocess(dicom_directory, x=512, y=512,
                     mode=None, processing='', mirroring_axes=None):
    """
    Processes a directory of dicom files into a numpy array.
    Does not standardize z-axis (slices) to support 2D/RNN models.
    :param dicom_directory: path to directory with dicom files
    :param x: x dimension of output
    :param y: y dimension of output
    :param mode: One of 'constant', 'edge', 'symmetric', 'reflect', 'wrap'
    :param processing: 'hu'
    :param mirroring_axes: 0 or more of ['lr', 'ud', 'fb']
    :return: np.array of [[slices, x, y], label]
    """
    from .three_d import three_d_preprocess
    # These relative imports are going to vary;
    # Need to update using init/setup files.
    return three_d_preprocess(dicom_directory=dicom_directory,
                              x=x, y=y, slices=-1,
                              mode=mode, processing=processing,
                              mirroring_axes=mirroring_axes)