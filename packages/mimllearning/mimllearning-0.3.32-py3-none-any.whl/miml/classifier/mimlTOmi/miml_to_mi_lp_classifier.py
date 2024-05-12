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

    def predict_bag(self, bag: Bag) -> np.ndarray:
        """
        Predict labels of a given bag

        Parameters
        ----------
        bag : Bag
            Bag to predict their labels

        Returns
        -------
        results : ndarray of shape (n_labels)
            Predicted labels of the bag
        """
        # super().predict_bag(bag)

        bags = self.transformation.transform_bag(bag)

        return self.predict(bags[0].get_features())

    def predict_proba(self, dataset_test: MIMLDataset):
        # TODO: DOC
        results = np.zeros((dataset_test.get_number_bags(), dataset_test.get_number_labels()))
        dataset = self.transformation.transform_dataset(dataset_test)
        results = self.classifier.predict_proba(dataset.get_features_by_bag())
        return results

    def evaluate(self, dataset_test: MIMLDataset) -> np.ndarray:
        """
        Evaluate the model on a test dataset

        Parameters
        ----------
        dataset_test : MIMLDataset
            Test dataset to evaluate the model on

        Returns
        ----------
        results : ndarray of shape (n_bags, n_labels)
            Predicted labels of dataset_test
        """
        # super().evaluate(dataset_test)

        dataset = self.transformation.transform_dataset(dataset_test)

        results = np.zeros((dataset_test.get_number_bags(), dataset_test.get_number_labels()))
        # Features are the same in all datasets
        for i, bag in enumerate(dataset.get_features_by_bag()):
            results[i] = self.predict(bag)

        return results
