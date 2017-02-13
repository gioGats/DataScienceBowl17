#NSTC Product Backlog

##Sprint 1 (Feb10 - Feb24): Image pre-processing and CNN

###Image Pre-Processing
This section takes a dicom file and outputs a 1D numpy array of a standard size.
######Subtasks:
- What exactly IS a dicom?  A collection of 2D scans plus header information?  Something else?
- Should we construct a 3D representation or present the sequence of 2D images? Can we try both?
- How do we handle variation in the data quality?  More scans per dicom vs fewer scans?  Color vs b&w?  Higher vs lower resolution?
- The last step of this segment should be numpy.reshape() to force 1D (easier to adjust later if necessary)

###Convolutional Neural Network
This section passes a 1D array through a series of layers and convolutional filters and outputs a high dimensional vector.
######Subtasks:
- What exactly IS a CNN?  How do we build and select (or manually force) filters?
- How do we train a CNN when the output isn't supervised?
- What existing CNNs are publicly available that could reduce training time or complexity (think Inception-v3 and transfer learning)?
- Initial implementations and training

##Sprint 2 (Feb24 - Mar10): RNN and custom anomaly detection

###Recurrent Neural Network

###Anomaly Detection

##Sprint 3 (Mar20 - Mar31): Custom CNN

##Sprint 4 (Mar31 - Apr14): Tuning

##Sprint 5 (Apr14 - Apr28): Deployment

