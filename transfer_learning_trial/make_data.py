from PIL import Image
import pydicom
# ISSUE package not loading properly, but is installed. Wtf?
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

    dicom_image = pydicom.read_file(source)
    pixel_array = dicom_image.pixel_array
    # FUTURE Consider selecting mode
    jpeg_image = Image.fromarray(pixel_array, mode=None)

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
    jpeg_image.save('%s.jpeg' % dest)


def get_dest(source):
    # Validation
    assert(isinstance(source, str))

    destination_string = 'transfer_trial/images'

    positive = assign_class(source)
    if positive:
        destination_string += '/positive'
    else:
        destination_string += '/negative'

    # TODO Increment filename as necessary
    filename = source

    destination_string += '/%s' % filename
    return destination_string


def assign_class(source):
    # TODO is this a positive or negative case?
    return True


if __name__ == '__main__':
    os.chdir('/nvme/stage1_data')
    if DEBUG:
        data_directory = 'sample_images'
    else:
        data_directory = 'stage1'

    if PROGRESS:
        total = len(os.listdir(data_directory))
        current = 0

    for patient_directory in os.listdir(data_directory):
        for dicom_filename in os.listdir('%s/%s' % (data_directory, patient_directory)):

            if PROGRESS:
                # noinspection PyUnboundLocalVariable
                print('\rImage conversion: %.2f' % (100 * (current/total)), end='')
                current += 1
            # noinspection PyBroadException
            try:
                to_jpeg(dicom_filename, get_dest(dicom_filename))
            except KeyboardInterrupt:
                break
            except Exception:
                handle_exception(sys.exc_info(), stdout=True, out_file=test_outfile)
    test_outfile.close()
