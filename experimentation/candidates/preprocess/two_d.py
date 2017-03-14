import os


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

if __name__ == '__main__':
    import unittest


    class TestTwoDPreprocess(unittest.TestCase):
        def setUp(self):
            self.params_2d = {'x': 100, 'y': 100, 'slices': -1, 'mode': None,
                              'processing': '', 'mirroring_axes': None}
            self.test_patient_dir = '/nvme/stage1_data/sample_images/0a0c32c9e08cc2ea76a71649de56be6d'

        def test_mirroring(self):
            # SPRINT2 visually test mirroring
            pass

        def test_two_d_preprocess(self):
            v = two_d_preprocess(self.test_patient_dir, x=self.params_2d['x'], y=self.params_2d['y'],
                                 mode=self.params_2d['mode'], processing=self.params_2d['processing'],
                                 mirroring_axes=self.params_2d['mirroring_axes'])
            assert(self.params_2d['mirroring_axes'] is None)  # Not written to check mirroring code yet
            self.assertEqual(v.shape, (2,))
            self.assertIsInstance(v[1], int)
            self.assertEqual(v[0].shape, (len(os.listdir(self.test_patient_dir)),
                                          self.params_2d['x'],
                                          self.params_2d['y']))

        def tearDown(self):
            pass

    unittest.main(verbosity=2)
