#!/usr/bin/env python
# ISSUE mudicom dependency gdcm dependency swig not Python3
import mudicom
import os
import sys
import traceback

DEBUG = True
PROGRESS = True
test_outfile = open('test.out', 'w')


def message(msg, log=False, out_file=None):
    # Validation
    if log and out_file is None:
        raise FileNotFoundError('message(): Must specify out file to log messages.')
    # Send msg to stdout
    print(msg)
    # Log if requested
    if log:
        out_file.write(msg)


def handle_exception(e, stdout=False, out_file=None):
    if stdout:
        traceback.print_exception(e[0], e[1], e[2])
    if out_file is not None:
        traceback.print_exception(e[0], e[1], e[2], file=out_file)


def to_jpeg(source, dest):
    # Validation
    assert(isinstance(source, str))
    assert(isinstance(dest, str))
    # ISSUE pydicom not converting properly
    print dest
    return
    """
    dicom_image = dicom.read_file(source)
    pixel_array = dicom_image.pixel_array
    # FUTURE Consider selecting mode
    jpeg_image = Image.fromarray(pixel_array, mode=None)
    """

    # FUTURE Consider using:
    """
    pixel_bytes = dicom_image.PixelData
    jpeg_image = Image.frombytes(mode=, size=, data=pixel_bytes)
    see:
    https://pydicom.readthedocs.io/en/latest/working_with_pixel_data.html
    http://pillow.readthedocs.io/en/4.0.x/reference/Image.html#PIL.Image.new
    http://pillow.readthedocs.io/en/4.0.x/handbook/concepts.html#concept-modes
    """
    # FUTURE Consider standardizing size, color, etc
    # ISSUE pydicom not converting properly
    # jpeg_image.save('%s.jpg' % dest)

    # ISSUE importing mudicom: ModuleNotFoundError: No module named 'gdcm'
    mu = mudicom.load(source)
    img = mu.image
    img.save_as_pil('%s.jpg' % dest)


def get_dest(patient):
    # Validation
    assert(isinstance(patient, str))

    destination_directory = 'transfer_trial/images'

    positive = assign_class(patient, labels_dict=LABELS_DICT)
    if positive:
        classification = 'positive'
    else:
        classification = 'negative'

    i = 0
    destination_string = '%s/%s/%s_%d' % (destination_directory, classification, patient, i)
    while True:
        if not os.path.exists(destination_string):
            return destination_string
        else:
            print('Incrementing')
            i += 1
            destination_string = '%s/%s/%s_%d' % (destination_directory, classification, patient, i)


def assign_class(patient, labels_dict=None):
    # Validation
    assert(isinstance(patient, str))

    if labels_dict is None:
        raise NotImplementedError('Non-labels_dict not implemented')
    return labels_dict[patient]


def make_labels_dict():
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
    os.chdir('/nvme/stage1_data')
    if DEBUG:
        data_directory = 'sample_images'
    else:
        data_directory = 'stage1'

    LABELS_DICT = make_labels_dict()

    if PROGRESS:
        total = len(os.listdir(data_directory))
        current = 0

    for patient_directory in os.listdir(data_directory):
        for dicom_filename in os.listdir('%s/%s' % (data_directory, patient_directory)):

            if PROGRESS:
                # noinspection PyUnboundLocalVariable
                # Python3
                # print('\rImage conversion: %.2f' % (100 * (current/total)), end='')
                # Python2
                print('\rImage conversion: %.2f' % (100 * (current/total))),
            # noinspection PyBroadException
            try:
                source_filename = '%s/%s/%s' % (data_directory, patient_directory, dicom_filename)
                to_jpeg(source_filename, get_dest(patient_directory))
            except KeyboardInterrupt:
                break
            except Exception:
                handle_exception(sys.exc_info(), stdout=True, out_file=test_outfile)
        if PROGRESS:
            current += 1
    test_outfile.close()
