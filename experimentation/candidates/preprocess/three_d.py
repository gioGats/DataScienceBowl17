

def three_d_preprocess(dicom_directory,
                       x=512, y=512, slices=100, channels=1, upsample='', downsample='', processing=''):
    # TODO Use str params for upsample, downsample, processing to assign functions to the following variables:
    # upsample_2d_function
    # upsample_3d_function
    # downsample_2d_function
    # downsample_3d_function
    # processing_function

    # TODO Bring all dicoms in dicom_directory into memory

    # TODO Process raw data values into a 2D numpy array (z, (x, y, channel))

    # TODO Process metadata

    # TODO Apply 2D resizing
    # for slice_array in slices:
    #     if (slice_array.x_shape < x) or (slice_array.y_shape < y) or (slice_array.channel_shape < channels):
    #         resized_array = upsample_2d_function(slice_array)
    #     elif (slice_array.x_shape > x) or (slice_array.y_shape > y) or (slice_array.channel_shape > channels):
    #         resized_array = downsample_2d_function(slice_array)
    #     else:
    #         raise Error Case
    # TODO Apply processing function
    #     processed_array = processing_function(resized_array)
    # TODO Replace slice_array with processed_array
    # (In the same data structure? This will be a single threaded operation, so priority to speed)

    # TODO 2D quick exit
    # if slices <= 0:
    # TODO Convert 3D array to 2D array
    # [(slice_array, label), (slice_array, label), (slice_array, label), (slice_array, label)]
    #    reshaped_array = resize_2d(slice_array)
    # TODO Ouput 2D array
    #     return reshaped_array

    # TODO Apply 3D resizing
    # else:
    #     if len(slice_array) < slices:
    #         resized_cube = upsample_3d_function(slice_array)
    #     elif len(slice_array) > slices:
    #         resized_cube = downsample_3d_function(slice_array)
    #     else:
    #         resized_cube = slice_array
    # TODO Output labelled 3D array
    # [resized_cube, label]
    # [(slice_array, slice_array, slice_array, slice_array), label]
    pass

