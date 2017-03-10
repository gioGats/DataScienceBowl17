

def two_d_preprocess(dicom_directory, x, y, channels, upsample, downsample, processing):
    from .three_d import three_d_preprocess
    return three_d_preprocess(dicom_directory=dicom_directory, x=x, y=y, slices=-1, channels=channels,
                              upsample=upsample, downsample=downsample, processing=processing)