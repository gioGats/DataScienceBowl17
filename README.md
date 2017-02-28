# DataScienceBowl17
Entries to the 2017 [Data Science Bowl](https://www.kaggle.com/c/data-science-bowl-2017/) competition for automated lung cancer detection, as part of CS 4620: Intelligent Systems

[Team Documents](https://drive.google.com/drive/folders/0B_qO3FJuQ8gyZTQ5R0pDbFN6U1E?usp=sharing)

#### Installation
Python 3.5+ is recommended.  Expect Python 3.6+.

Training and experimentation is done in the /experimentation directory.  Two production models will have their own directories for competition predictions.  Experimentation and production requirements may vary; see individual directories for requirements.

From a command line in each directory, 'sudo pip3 install -r requirements.txt' will install latest versions of required packages.
This will attempt to install TensorFlow v1.0.  This installation will likely fail if previous versions of tensorflow are installed.
Installing tensorflow-gpu is strongly recommended for experimentation and encouraged for production.

Follow [the TensorFlow installation guide](https://www.tensorflow.org/install/) for assistance.
