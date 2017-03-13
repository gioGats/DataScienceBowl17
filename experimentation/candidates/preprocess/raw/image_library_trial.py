import cv2
from skimage import transform
import numpy as np
import time
import os
import pickle


def test_arrays(n=100, x=512, y=512, slices=100, channels=3, dtype='int16'):
    return np.random.randint(low=0, high=128, size=(n, slices, x, y, channels), dtype=dtype)


if __name__ == '__main__':
    this_test_arrays = test_arrays()
    timings = dict(skimage_all=[], skimage_patients=[], skimage_slices=[],
                   cv2_opt_all=[], cv2_opt_patients=[], cv2_opt_slices=[],
                   cv2_all=[], cv2_patients=[], cv2_slices=[])

    # OPENCV OPTIMIZED TRIAL
    i = 0
    cv2.setUseOptimized(True)
    all_start = time.time()
    for array in this_test_arrays:
        patient_start = time.time()
        j = 0
        for slice in array:
            slice_start = time.time()
            # Resize down
            down = cv2.resize(slice, (100, 100))
            # Resize up
            up = cv2.resize(slice, (1000, 1000))

            # FUTURE Flip vertical

            # FUTURE Flip horizontal

            # FUTURE Some fancy filter
            j += 1
            print("\rOPENCV OPT TRIAL | patient %d of 100 | slice %d of 100" % (i, j), end='')
            timings['cv2_opt_slices'].append(time.time()-slice_start)
        i += 1
        timings['cv2_opt_patients'].append(time.time()-patient_start)

    timings['cv2_opt_all'].append(time.time()-all_start)
    print()
    for k in ['cv2_opt_all', 'cv2_opt_patients', 'cv2_opt_slices']:
        v = timings[k]
        print('%s\nMax: %.2f; Mean: %.2f; Std: %.2f; Min: %.2f\n' % (k, np.max(v), np.mean(v), np.std(v), np.min(v)))

    # OPENCV UNOPTIMIZED TRIAL
    i = 0
    cv2.setUseOptimized(False)
    all_start = time.time()
    for array in this_test_arrays:
        patient_start = time.time()
        j = 0
        for slice in array:
            slice_start = time.time()
            # Resize down
            down = cv2.resize(slice, (1000, 1000))
            # Resize up
            up = cv2.resize(slice, (1000, 1000))

            # FUTURE Flip vertical

            # FUTURE Flip horizontal

            # FUTURE Some fancy filter
            j += 1
            print("\rOPENCV TRIAL | patient %d of 100 | slice %d of 100" % (i, j), end='')
            timings['cv2_slices'].append(time.time()-slice_start)
        i += 1
        timings['cv2_patients'].append(time.time()-patient_start)
    timings['cv2_all'].append(time.time()-all_start)
    print()
    for k in ['cv2_all', 'cv2_patients', 'cv2_slices']:
        v = timings[k]
        print('%s\nMax: %.2f; Mean: %.2f; Std: %.2f; Min: %.2f\n' % (k, np.max(v), np.mean(v), np.std(v), np.min(v)))

    # SKIMAGE TRIAL
    i = 0
    print()
    all_start = time.time()
    for array in this_test_arrays:
        patient_start = time.time()
        j = 0
        for slice in array:
            slice_start = time.time()
            # Resize down
            down = transform.resize(slice, (100, 100, 1))
            # Resize up
            up = transform.resize(slice, (1000, 1000, 3))

            # FUTURE Flip vertical

            # FUTURE Flip horizontal

            # FUTURE Some fancy filter

            j += 1
            print("\rSKIMAGE TRIAL | patient %d of 100 | slice %d of 100" % (i, j), end='')
            timings['skimage_slices'].append(time.time()-slice_start)
        i += 1
        timings['skimage_patients'].append(time.time()-patient_start)
    timings['skimage_all'].append(time.time()-all_start)
    print()
    for k in ['skimage_all', 'skimage_patients', 'skimage_slices']:
        v = timings[k]
        print('%s\nMax: %.2f; Mean: %.2f; Std: %.2f; Min: %.2f\n' % (k, np.max(v), np.mean(v), np.std(v), np.min(v)))

    with open('timings.pkl', 'wb') as f:
        pickle.dump(timings, f)
        f.close()

"""
    for k in timings.keys():
        v = timings[k]
        print('%s\nMax: %.2f; Mean: %.2f; Std: %.2f; Min: %.2f\n' % (k, np.max(v), np.mean(v), np.std(v), np.min(v)))
"""
