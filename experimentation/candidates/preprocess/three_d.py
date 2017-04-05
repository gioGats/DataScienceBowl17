import numpy as np
import pandas as pd
import dicom
from skimage.transform import resize
import os


def three_d_preprocess(dicom_directory,
                       x=512, y=512, slices=100,
                       mode=None, processing='', mirroring=False, blurring=False):
    """
    Processes a directory of dicom files into a numpy array. (3D)
    :param dicom_directory: path to directory with dicom files
    :param x: x dimension of output
    :param y: y dimension of output
    :param slices: number of slices in output
    :param mode: None or one of 'constant', 'edge', 'symmetric', 'reflect', 'wrap'
    :param processing: '' defaults to 'hu'; other preprocessing tbd
    :param mirroring_axes: None or one or more of ['lr', 'ud', 'fb']
    :return: np.array of [[slices, x, y], label]
    """
    # Validate input, passed directly to skimage.transform.resize()
    if mode is None:
        mode = 'constant'
    elif mode not in ['constant', 'edge', 'symmetric', 'reflect', 'wrap']:
        raise NotImplementedError('%s not a valid resizing mode' % mode)

    # Bring all dicoms in dicom_directory into memory
    patient_array = load_scan(dicom_directory)

    if processing == '' or 'hu':
        # adjust pixel values  with processing function
        patient_array = get_pixels_hu(patient_array)

    patient_id = dicom_directory.split('/')[-1]
    label = int(patient_id[-1])
    # TODO Troubleshoot patient '0b20184e0cd497028bdd155d9fb42dc9'

    # Apply resizing
    patient_array = resize_image(patient_array, shape=(x, y, slices), mode=mode)
    return_arrays = np.array([initial_array, label], dtype='int16')

    if mirroring:
        return_arrays = mirror_array(return_arrays)
    if blurring:
        return_arrays = blur_array(return_arrays)
    return return_arrays


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


def mirror_array(initial_array):
    return_arrays = initial_array
    for arr in return_arrays:
        array_to_add = np.array([np.flip(arr, 1), label])
        return_arrays = np.vstack((return_arrays, array_to_add))
    for arr in return_arrays:
        array_to_add = np.array([np.flip(arr, 2), label])
        return_arrays = np.vstack((return_arrays, array_to_add))
    for arr in return_arrays:
        array_to_add = np.array([np.flip(arr, 0), label])
        return_arrays = np.vstack((return_arrays, array_to_add))
    return return_arrays


def blur_array(initial_arrays):
    # TODO Blurring
    return initial_arrays


def resize_image(patient_array, shape, mode):
    if shape[2] <= 0:
        shape = (shape[0], shape[1], len(patient_array))
    patient_array = resize(patient_array, shape, mode=mode)
    patient_array = np.swapaxes(patient_array, 0, 2)
    return patient_array

if __name__ == '__main__':
    import unittest


    class TestThreeDPreprocess(unittest.TestCase):
        def setUp(self):
            self.params_3d = {'x': 100, 'y': 100, 'slices': 50, 'mode': None,
                              'processing': '', 'mirroring': False, 'blurring': False}
            self.test_patient_dir = '/nvme/stage1_data/sample_images/0a0c32c9e08cc2ea76a71649de56be6d'

        def test_get_label(self):
            self.assertEqual(get_label('0a0c32c9e08cc2ea76a71649de56be6d'), 0)
            self.assertEqual(get_label('0c60f4b87afcb3e2dfa65abbbf3ef2f9'), 1)
            self.assertEqual(get_label('0d2fcf787026fece4e57be167d079383'), 0)
            self.assertEqual(get_label('0d19f1c627df49eb223771c28548350e'), 0)
            self.assertEqual(get_label('0a38e7597ca26f9374f8ea2770ba870d'), 0)

        def test_load_scan(self):
            # FUTURE unit test load_scan
            pass

        def test_get_pixels_hu(self):
            patient_array = get_pixels_hu(load_scan(self.test_patient_dir))
            self.assertEqual(patient_array.dtype, 'int16')
            self.assertEqual(len(patient_array.shape), 3)
            self.assertEqual(patient_array.shape[0], len(os.listdir(self.test_patient_dir)))
            self.assertEqual(patient_array[0].shape, (patient_array.shape[1], patient_array.shape[2]))
            self.assertIsInstance(patient_array[0][0][0], np.int16)

            # FUTURE unit test get_pixels_hu in more depth

        def test_mirror_array(self):
            self.fail('Not implemented')

        def test_blur_array(self):
            self.fail('Not implemented')

        def test_three_d_preprocess(self):
            v = three_d_preprocess(self.test_patient_dir, x=self.params_3d['x'], y=self.params_3d['y'],
                                   slices=self.params_3d['slices'], mode=self.params_3d['mode'],
                                   processing=self.params_3d['processing'],
                                   mirroring=self.params_3d['mirroring'], blurring=self.params_3d['blurring'])
            assert(self.params_3d['mirroring'] is None)  # Not written to check mirroring code yet
            assert(self.params_3d['blurring'] is None)  # Not written to check blurring code yet
            self.assertEqual(v.shape, (2,))
            self.assertIsInstance(v[1], int)
            self.assertEqual(v[0].shape, (self.params_3d['slices'],
                                          self.params_3d['x'],
                                          self.params_3d['y']))

        def tearDown(self):
            pass


    unittest.main(verbosity=2)
