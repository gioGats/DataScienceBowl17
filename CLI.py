# FUTURE Command-Line Interface for running sub-scripts


class CLI(object):
    def __init__(self):
        pass


class ClassifierInterface(object):
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

    def make_submission(self, patient_dict, output='stage1_submission.csv'):
        """
        Given a dictionary of patient_id: list of dicoms, generate a submission file
        :param patient_dict: dict
        :param output: str filename to save to, default
        """
        output_file = open(output, 'w')
        output_file.write('id,cancer\n')
        for patient_id in patient_dict.keys():
            output_file.write('%s,%.2f\n' % (patient_id, self.classify(patient_dict[patient_id])))
        output_file.close()