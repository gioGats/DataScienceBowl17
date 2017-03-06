# FUTURE Command-Line Interface for running sub-scripts
import pickle


class CLI(object):
    def __init__(self):
        pass


class ClassifierInterfaces(object):
    def __init__(self, model):
        if model == '1':
            with open('production_1/model.pkl', 'rb') as f:
                self.model = pickle.load(f)
                f.close()
            from production_1.preprocess import two_d_preprocess as preprocess
        elif model == '2':
            with open('production_2/model.pkl', 'rb') as f:
                self.model = pickle.load(f)
                f.close()
            from production_2.preprocess import three_d_preprocess as preprocess
        else:
            raise NotImplementedError

    def classify(self, patient_dir):
        """
        Given a directory named for patient id and continaing a series of dicom slices,
        return probability that patient is diagnosed with lung cancer in the next 12 months.
        :param patient_dir: path to patient directory
        :return: float in range [0,1]
        """
        return self.model.predict(preprocess(patient_dir))

    def make_submission(self, patient_list, output='stage1_submission.csv'):
        """
        Given a list of patient_ids, generate a submission file
        :param patient_list: list of str
        :param output: str filename to save to, default
        """
        output_file = open(output, 'w')
        output_file.write('id,cancer\n')
        for patient_id in patient_list:
            output_file.write('%s,%.2f\n' % (patient_id, self.classify(patient_id)))
        output_file.close()

if __name__ == '__main__':
    pass
    # patient_list = [id1, id2, ..., idn]
    # ci = ClassifierInterfaces()
    # ci.make_submission(patient_list, output='patient_results.txt')
