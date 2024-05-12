import numpy as np
from copy import deepcopy
from ...data import Bag
from ...data import MIMLDataset


class LabelPowersetTransformation:
    """
    Class that performs a binary relevance transformation to convert a MIMLDataset class to numpy ndarray.
    """

    def __init__(self):
        self.dataset = None

    def transform_dataset(self, dataset: MIMLDataset) -> MIMLDataset:
        """
        Transform the dataset to multiinstance datasets dividing the original dataset into n datasets with a single
        label, where n is the number of labels.

        Returns
        -------

        datasets: MIMLDataset
            Multi instance dataset

        """
        self.dataset = dataset
        number_labels = self.dataset.get_number_labels()
        labels = self.dataset.get_labels_by_bag()
        labels_transformed = []

        for label in labels:
            labels_transformed.append(np.dot(label, np.flip(2 ** np.arange(len(label)))))

        for i in range(number_labels-1, 0, -1):
            dataset.delete_attribute(self.dataset.get_number_features()+i)

        for i in range(dataset.get_number_bags()):
            bag = dataset.get_bag(i)
            for j in range(bag.get_number_instances()):
                dataset.set_attribute(i, j, dataset.get_number_attributes()-1, labels_transformed[i])

        dataset.set_labels_name(["lp label"])

        return dataset

    def transform_bag(self, bag: Bag) -> Bag:
        """
        Transform miml bag to multi instance bags

        Parameters
        ----------
        bag :
            Bag to be transformed to multiinstance bag

        Returns
        -------
        bags : list[Bag]
            List of n_labels transformed bags

        """
        if bag.dataset is None:
            raise Exception("Can't transform a bag without an assigned dataset, because we wouldn't have info about "
                            "the features and labels")

        transformed_bag = deepcopy(bag)
        for j in range(bag.get_number_labels(), 0, -1):
            transformed_bag.dataset.attributes.pop(list(transformed_bag.dataset.attributes)[-1])
            transformed_bag.data = np.delete(transformed_bag.data, bag.get_number_features()+j, axis=1)

        transformed_bag.dataset.set_labels_name(["lp label"])

        return transformed_bag
