# FUTURE Command-Line Interface for running sub-scripts


class CLI(object):
    def __init__(self):
        pass


class Classifier(object):
    def __init__(self):
        pass

    def classify(self, dicom_list):
        """
        Given a list of dicom images from a patient,
        return probability that patient is diagnosed with lung cancer in the next 12 months.
        :param dicom_list: list of dicom images
        :return: float in range [0,1]
        """
        raise NotImplementedError
