#!/usr/bin/env python
# FUTURE mudicom dependency gdcm dependency swig not Python3; Upgrade to pydicom for improved support
import mudicom
import os
import sys
import traceback
"""
Converts dicom images organized by patient to jpg images organized by classification.
Data pre-processing required for transfer-learning on Inception-v3 via TensorFlow
See:
https://research.googleblog.com/2016/03/train-your-own-image-classifier-with.html
https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/image_retraining/retrain.py
"""


# Use sample directory (1.4GB) instead of main directory (140GB)
DEBUG = False
# Print progress reports to terminal
PROGRESS = True
# File to save error messages
test_outfile = open('test.out', 'w')


def message(msg, stdout=True, out_file=None):
    """
    Wrapper for text output
    :param msg: str to output
    :param stdout: bool, send msg to stout?
    :param out_file: file to write msg to, does not write if None
    """
    if stdout:
        print(msg)
    if out_file is not None:
        out_file.write(msg)


def handle_exception(e, stdout=False, out_file=None):
    """
    Wrapper for exception handling
    :param e: Exception object
    :param stdout: bool, report to stdout?
    :param out_file: file to write e to, does not write if None
    """
    if stdout:
        traceback.print_exception(e[0], e[1], e[2])
    if out_file is not None:
        traceback.print_exception(e[0], e[1], e[2], file=out_file)


def to_jpeg(source, dest):
    """
    Converts a dicom at source to a jpg at dest
    :param source: str
    :param dest: str
    """
    # Validation
    assert(isinstance(source, str))
    assert(isinstance(dest, str))

    # FUTURE Replace mudicom with pydicom for native Python3 support
    mu = mudicom.load(source)
    img = mu.image
    # img.save_as_plt returns True if successful
    if img.save_as_plt(dest):
        return
    else:
        print('Save %s at %s -- FAILED' % (source, dest))


def get_dest(patient):
    """
    Get the destination of the next jpg image to save for patient
    :param patient: str, patient id
    :return: str
    """
    # Validation
    assert(isinstance(patient, str))

    destination_directory = 'transfer_trial/images'

    # Assign class
    positive = assign_class(patient, labels_dict=LABELS_DICT)
    if positive:
        classification = 'positive'
    else:
        classification = 'negative'

    # Increment filename
    i = 0
    destination_string = '%s/%s/%s_%d.jpg' % (destination_directory, classification, patient, i)
    while True:
        if not os.path.exists(destination_string):
            return destination_string
        else:
            i += 1
            destination_string = '%s/%s/%s_%d.jpg' % (destination_directory, classification, patient, i)


def assign_class(patient, labels_dict=None):
    """
    Assign a patient to their respective class
    :param patient: str, patient id
    :param labels_dict: dict, see make_labels_dict
    :return: boolean, True if positive
    """
    # Validation
    assert(isinstance(patient, str))

    if labels_dict is None:
        raise NotImplementedError('Non-labels_dict not implemented')
    try:
        return labels_dict[patient]
    except KeyError:
        raise KeyError("Patient '%s' not in labels dictionary" % patient)


def make_labels_dict():
    """
    Makes a labels dictionary from provided csv file
    :return: dict
    """
    labels_dict = {}
    labels_file = open('stage1_labels.csv', 'r')
    for line in labels_file:
        if line[:2] == 'id':
            continue
        line_list = line.replace('\n', '').split(',')
        patient = line_list[0]
        value = line_list[1]
        if value == '1':
            labels_dict[patient] = True
        elif value == '0':
            labels_dict[patient] = False
        else:
            raise ValueError('Patient value unknown!\nid: %s' % patient)
    return labels_dict


if __name__ == '__main__':
    # change to deployment directory
    os.chdir('/nvme/stage1_data')
    if DEBUG:
        data_directory = 'sample_images'
    else:
        data_directory = 'stage1'

    # Global labels dictionary
    LABELS_DICT = make_labels_dict()

    if PROGRESS:
        total = len(os.listdir(data_directory))
        current = 0

    for patient_directory in os.listdir(data_directory):
        if PROGRESS:
            # noinspection PyUnboundLocalVariable
            # Future Python3 conversion
            # print('\rImage conversion: %.2f' % (100 * (current/total)), end='')
            # Python2 Patch
            print('Image conversion: %d of %d' % (current, total))
            current += 1
        for dicom_filename in os.listdir('%s/%s' % (data_directory, patient_directory)):
            # noinspection PyBroadException
            try:
                source_filename = '%s/%s/%s' % (data_directory, patient_directory, dicom_filename)
                to_jpeg(source_filename, get_dest(patient_directory))
            except KeyError:
                # FUTURE handle missing key for patient '0b20184e0cd497028bdd155d9fb42dc9'
                continue
            except KeyboardInterrupt:
                break
            except Exception:
                handle_exception(sys.exc_info(), stdout=False, out_file=test_outfile)
    test_outfile.close()
