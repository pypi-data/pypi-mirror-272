import numpy as np
from copy import deepcopy

from .miml_to_mi_classifier import MIMLtoMIClassifier
from ...transformation import LabelPowersetTransformation
from ...data import Bag
from ...data import MIMLDataset


class MIMLtoMILPClassifier(MIMLtoMIClassifier):
    """
    Class to represent a multiinstance classifier
    """

    def __init__(self, classifier) -> None:
        """
        Constructor of the class MIMLtoMILPClassifier

        Parameters
        ----------
        classifier
            Specific classifier to be used
        """
        super().__init__(classifier)
        self.transformation = LabelPowersetTransformation()

    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """
        Training the classifier

        Parameters
        ----------
        dataset_train: MIMLDataset
            Dataset to train the classifier
        """

        dataset = self.transformation.transform_dataset(dataset_train)

        self.classifier.fit(dataset.get_features_by_bag(), dataset.get_labels_by_bag())

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Predict labels of given data

        Parameters
        ----------
        x : ndarray of shape (n_instances, n_features)
            Data to predict their labels

        Returns
        -------
        results : ndarray of shape (n_labels)
            Predicted labels
        """
        # Prediction of each label
        results = self.classifier.predict(x)
        binary_str = np.binary_repr(results, width=self.transformation.dataset.get_number_labels())
        return np.array([int(bit) for bit in binary_str])

    def predict_proba(self, dataset_test: MIMLDataset):
        # TODO: DOC
        return self.classifier.predict_proba(dataset_test.get_features_by_bag())

