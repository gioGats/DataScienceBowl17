import numpy as np
import pandas as pd
import dicom
import os
import scipy.ndimage
import matplotlib.pyplot as plt

from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.ndimage.filters import gaussian_filter, gaussian_filter1d, \
    median_filter, convolve, laplace, minimum_filter, maximum_filter
from random import randint


def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
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


# ----------------------------------------------------------------------Multiple preprocessing functions------------------------------------------------------------------

def flipX(patient_pixels):
    a = np.flip(patient_pixels, 1)
    return a


def flipY(
        patient_pixels):  # Makes for really wonky images for some reason... Don't recommend. ***Works really well with 3D. No idea.
    a = np.flipud(patient_pixels)
    return a


def blurGaussian(patient_pixels, x):  # anything greater than sigma 4 makes a really bad picutre. Plays well with 3D
    a = gaussian_filter(patient_pixels, sigma=x)
    return a


def blurMedian(patient_pixels,
               x):  # pretty unrealistically long computation time for anything above 3. 2 or 3 could give us a readable, but different image.
    a = median_filter(patient_pixels, x)
    return a


def blurLaplace(patient_pixels):  # This one could be interesting to play with. Doesn't play well with 3D
    a = laplace(patient_pixels, mode='mirror')
    return a


def blurMax(patient_pixels, x):  # Standard max blurring. We'll use this.
    a = maximum_filter(patient_pixels, x, mode='wrap')
    return a


def blurMin(patient_pixels, x):  # Standard min blurring. We'll use this.
    a = minimum_filter(patient_pixels, x)
    return a


def modeSelection():  # this is just here for reference, obviously we'd call MODES[randint(0,4)] inline if we wanted to randomize it a bit.
    return MODES[randint(0, 4)]


if __name__ == '__main__':
    # From above function definitions
    INPUT_FOLDER = 'C:/KaggleData/sample_images/'
    MODES = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']

    patients = os.listdir(INPUT_FOLDER)
    patients.sort()

    # From below function definitions
    first_patient = load_scan(INPUT_FOLDER + patients[0])
    first_patient_pixels = get_pixels_hu(first_patient)
    a = blurMin(first_patient_pixels, 3, modeSelection())

    fig = plt.figure()
    y = fig.add_subplot(1, 2, 1)
    y.imshow(first_patient_pixels[80], cmap=plt.cm.inferno)
    y = fig.add_subplot(1, 2, 2)
    y.imshow(a[80], cmap=plt.cm.inferno)

    plt.show()
