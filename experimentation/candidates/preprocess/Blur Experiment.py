'''
Created on Mar 10, 2017

@author: Charlie Neff
'''


import numpy as np
import pandas as pd
import dicom
import os
import scipy.ndimage
import matplotlib.pyplot as plt


from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.ndimage.filters import gaussian_filter, gaussian_filter1d,\
    median_filter, convolve, laplace, minimum_filter, maximum_filter
from random import randint
from pywt._thresholding import threshold



INPUT_FOLDER = 'C:/KaggleData/sample_images/'
MODES = ['reflect', 'constant', 'nearest', 'mirror', 'wrap']

patients = os.listdir(INPUT_FOLDER)
patients.sort()

def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
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

#----------------------------------------------------------------------Multiple preprocessing functions------------------------------------------------------------------
#For all blurs, very low pixel values are necessary for 3d, however higher will be needed for 2d.

def flipX(patient_pixels):
    a = np.flip(patient_pixels, 1)
    return a

def flipY(patient_pixels): #Makes for really wonky images for some reason... Don't recommend.
    a = np.flipud(patient_pixels)
    return a

def blurGaussian(patient_pixels, x): #anything greater than sigma 4 makes a really bad picutre.
    a = gaussian_filter(patient_pixels, sigma=x)
    return a

def blurMedian(patient_pixels, x): #pretty unrealistically long computation time for anything above 3. 2 or 3 could give us a readable, but different image.
    a = median_filter(patient_pixels, x)
    return a

def blurLaplace(patient_pixels): #This one could be interesting. Doesn't play well with 3D
    a = laplace(patient_pixels, mode='mirror')
    return a

def blurMax(patient_pixels, x): #Standard max blurring. We'll use this.
    a = maximum_filter(patient_pixels, x, mode='wrap')
    return a

def blurMin(patient_pixels, x): #Standard min blurring. We'll use this.
    a = minimum_filter(patient_pixels, x) 
    return a

def modeSelection():   #this is just here for reference, obviously we'd call MODES[randint(0,4)] inline if we wanted to randomize it a bit. 
    return MODES[randint(0,4)]
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def resample(image, scan, new_spacing=[1,1,1]):
    spacing = np.array([scan[0].SliceThickness] + scan[0].PixelSpacing, dtype=np.float32)
    
    resize_factor= spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')
    
    return image, new_spacing

def plot_3d(image, threshold=-300):
    p = image.transpose(2,1,0)
    
    verts, faces = measure.marching_cubes_classic(p, threshold)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    mesh = Poly3DCollection(verts[faces], alpha=0.70)
    face_color = [0.45, 0.45, 0.75]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, p.shape[0])
    ax.set_ylim(0, p.shape[1])
    ax.set_zlim(0, p.shape[2])

    plt.show()

def largest_label_volume(im, bg=-1):
    vals, counts = np.unique(im, return_counts=True)
    
    counts = counts[vals!= bg]
    vals = vals[vals != bg]
    
    if len(counts) > 0:
        return vals[np.argmax(counts)]
    else:
        return None
    
def segment_lung_mask(image, fill_lung_structures=True):
    
    # not actually binary, but 1 and 2. 
    # 0 is treated as background, which we do not want
    binary_image = np.array(image > -320, dtype=np.int8)+1
    labels = measure.label(binary_image)
    
    # Pick the pixel in the very corner to determine which label is air.
    #   Improvement: Pick multiple background labels from around the patient
    #   More resistant to "trays" on which the patient lays cutting the air 
    #   around the person in half
    background_label = labels[0,0,0]
    
    #Fill the air around the person
    binary_image[background_label == labels] = 2
    
    
    # Method of filling the lung structures (that is superior to something like 
    # morphological closing)
    if fill_lung_structures:
        # For every slice we determine the largest solid structure
        for i, axial_slice in enumerate(binary_image):
            axial_slice = axial_slice - 1
            labeling = measure.label(axial_slice)
            l_max = largest_label_volume(labeling, bg=0)
            
            if l_max is not None: #This slice contains some lung
                binary_image[i][labeling != l_max] = 1

    
    binary_image -= 1 #Make the image actual binary
    binary_image = 1-binary_image # Invert it, lungs are now 1
    
    # Remove other air pockets insided body
    labels = measure.label(binary_image, background=0)
    l_max = largest_label_volume(labels, bg=0)
    if l_max is not None: # There are air pockets
        binary_image[labels != l_max] = 0
 
    return binary_image    


first_patient = load_scan(INPUT_FOLDER + patients[0])
first_patient_pixels = get_pixels_hu(first_patient)
first_patient_pixels = blurMax(first_patient_pixels, 3)

pix_resampled, spacing = resample(first_patient_pixels, first_patient, [1,1,1])
segmented_lungs = segment_lung_mask(pix_resampled, False)
segmented_lungs_fill = segment_lung_mask(pix_resampled, True)

plot_3d(segmented_lungs_fill - segmented_lungs, 0)


#a = blurMin(first_patient_pixels, 3, modeSelection())

'''
fig = plt.figure()
y=fig.add_subplot(1,2,2)
y.imshow(pix_resampled[80], cmap=plt.cm.inferno)
y=fig.add_subplot(1,2,1)
y.imshow(first_patient_pixels[80], cmap=plt.cm.inferno)

plt.show()
'''
