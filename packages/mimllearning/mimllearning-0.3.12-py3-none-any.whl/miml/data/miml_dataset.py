import random

import numpy as np

from .bag import Bag
from .instance import Instance


class MIMLDataset:
    """
    Class to manage MIML data obtained from datasets
    """

    def __init__(self) -> None:
        """
        Constructor of the class MIMLDataset
        """
        self.name = "undefined"
        self.attributes = dict()
        self.data = dict()

    def set_name(self, name) -> None:
        """
        Set function for dataset name

        Parameters
        ----------
        name : str
            Name of the dataset
        """
        self.name = name

    def get_name(self) -> str:
        """
         Get function for dataset name

        Returns
        ----------
        name : str
            Name of the dataset
        """
        return self.name

    def get_attributes_name(self) -> list[str]:
        """
        Get attributes name

        Returns
        ----------
        attributes : list[str]
            Attributes name of the dataset
        """
        return list(self.attributes.keys())

    def get_attributes(self) -> np.ndarray:
        """
        Get attributes values of the dataset

        Returns
        -------
        attributes data: ndarray of shape (n_instances, n_attributes)
            Values of the attributes of the dataset
        """
        return np.hstack((self.get_features(), self.get_labels()))

    def get_number_attributes(self) -> int:
        """
        Get numbers of attributes of the bag

        Returns
        ----------
        numbers of attributes: int
            Numbers of attributes of the bag
        """
        return len(self.get_attributes_name())

    def set_features_name(self, features: list[str]) -> None:
        """
        Set function for dataset features name

        Parameters
        ----------
        features : list[str]
            List of the features name of the dataset
        """
        if len(self.attributes) != 0:
            for feature in self.get_features_name():
                if self.attributes[feature] == 0:
                    self.attributes.pop(feature)
        for feature in features:
            self.attributes[feature] = 0

    def get_features_name(self) -> list[str]:
        """
        Get function for dataset features name

        Returns
        ----------
        attributes : list[str]
            Attributes name of the dataset
        """
        features = []
        for feature in self.attributes.keys():
            if self.attributes[feature] == 0:
                features.append(feature)
        return features

    def get_features(self) -> np.ndarray:
        """
        Get features values of the dataset

        Returns
        -------
        features: ndarray of shape (n_instances, n_features)
            Values of the features of the dataset
        """
        features = np.zeros((self.get_number_instances(), self.get_number_features()))
        count = 0
        for key in self.data.keys():
            for instance in self.get_bag(key).get_features():
                features[count] = instance
                count += 1
        return features

    def get_features_by_bag(self) -> np.ndarray:
        # TODO: Doc
        features = []
        for key in self.data.keys():
            features.append(self.get_bag(key).get_features())
        return np.array(features, dtype=object)

    def get_number_features(self) -> int:
        """
        Get numbers of attributes of the dataset

        Returns
        ----------
         numbers of attributes: int
            Numbers of attributes of the dataset
        """
        return len(self.get_features_name())

    def set_labels_name(self, labels: list[str]) -> None:
        """
        Set function for dataset labels name

        Parameters
        ----------
        labels: list[str]
            List of the labels name of the dataset
        """
        if len(self.attributes) != 0:
            for label in self.get_labels_name():
                if self.attributes[label] == 1:
                    self.attributes.pop(label)
        for label in labels:
            self.attributes[label] = 1

    def get_labels_name(self) -> list[str]:
        """
        Get function for dataset labels name

        Returns
        ----------
        labels : list[str]
            Labels name of the dataset
        """
        labels = []
        for attribute in self.attributes.keys():
            if self.attributes[attribute] == 1:
                labels.append(attribute)
        return labels

    def get_labels(self):
        """
        Get labels values of the dataset

        Returns
        -------
        labels: ndarray of shape (n_instances, n_labels)
            Values of the labels of the dataset
        """
        labels = np.zeros((self.get_number_instances(), self.get_number_labels()))
        count = 0
        for key in self.data.keys():
            for instance in self.get_bag(key).get_labels():
                labels[count] = instance
                count += 1
        return labels

    def get_labels_by_bag(self):
        """
        Get labels values of the dataset

        Returns
        -------
        labels : ndarray of shape (n_bags, n_labels)
            Values of the labels of the dataset
        """
        labels = np.zeros((self.get_number_bags(), self.get_number_labels()))
        for bag_index, key in enumerate(self.data.keys()):
            labels[bag_index] = self.get_bag(key).get_labels()[0]
        return labels

    def get_number_labels(self) -> int:
        """
        Get numbers of labels of the dataset

        Returns
        ----------
        numbers of labels: int
            Numbers of labels of the dataset
        """
        return len(self.get_labels_name())

    def get_bag(self, bag) -> Bag:
        """
        Get data of a bag of the dataset

        Parameters
        ----------
        bag: int/str
            Index or key of the bag to be obtained

        Returns
        ----------
        bag: Bag
            Instance of Bag class
        """
        if isinstance(bag, int):
            return list(self.data.values())[bag]
        elif isinstance(bag, str):
            return self.data[bag]
        print(type(bag))
        raise Exception("The bag can be obtained using an index (int) or his key (str)")

    def get_number_bags(self) -> int:
        """
        Get numbers of bags of the dataset

        Returns
        ----------
        numbers of bags: int
            Numbers of bags of the dataset
        """
        return len(self.data)

    def add_bag(self, bag: Bag) -> None:
        """
        Add a bag to the dataset

        Parameters
        ----------
        bag : Bag
            Instance of Bag class to be added
        """
        if bag.get_number_attributes() == self.get_number_attributes():
            bag.set_dataset(self)
            self.data[bag.key] = bag
        else:
            raise Exception("The bag doesn't have the same attributes as the dataset")

    def delete_bag(self, key_bag: str) -> None:
        """
        Delete a bag of the dataset

        Parameters
        ----------
        key_bag : str
            Key of the bag to be deleted
        """
        self.data.pop(key_bag)

    def get_instance(self, key_bag, index_instance) -> Instance:
        """
        Get an Instance of the dataset

        Parameters
        ----------
        key_bag : str
            Key of the bag
            
        index_instance : int
            Index of the instance in the bag

        Returns
        -------
        instance : Instance
            Instance of Instance class
        """
        return self.get_bag(key_bag).get_instance(index_instance)

    def get_number_instances(self) -> int:
        """
        Get numbers of instances of the dataset

        Returns
        ----------
        numbers of instances: int
            Numbers of instances of the dataset
        """
        return sum(self.data[bag].get_number_instances() for bag in self.data.keys())

    def add_instance(self, bag, instance: Instance) -> None:
        """
        Add an Instance to a Bag of the dataset

        Parameters
        ----------
        bag : int/str
            Index or key of the bag where the instance will be added

        instance : Instance
            Instance of Instance class to be added
        """
        #TODO: Test if it works
        new_bag = self.get_bag(bag)
        new_bag.add_instance(instance)
        self.data[new_bag.key] = new_bag

    def delete_instance(self, bag, index_instance: int) -> None:
        """
        Delete an instance of a bag of the dataset

        Parameters
        ----------
        bag : int/str
            Index or key of the bag which contains the instance to be deleted

        index_instance : int
            Index of the instance to be deleted
        """
        new_bag = self.get_bag(bag)
        new_bag.delete_instance(index_instance)
        self.data[new_bag.key] = new_bag

    def get_attribute(self, bag, instance, attribute) -> float:
        """
        Get value of an attribute of the bag

        Parameters
        ----------
        bag : str
            Key of the bag which contains the attribute

        instance : int
            Index of the instance in the bag

        attribute : int/str
            Index/Name of the attribute

        Returns
        -------
        value : float
            Value of the attribute
        """
        return self.get_instance(bag, instance).get_attribute(attribute)

    def set_attribute(self, bag, index_instance: int, attribute, value: float) -> None:
        """
        Update value from attributes

        Parameters
        ----------
        bag : int/str
            Index or key of the bag of the dataset

        index_instance : int
            Index of the instance

        attribute: int/str
            Attribute of the dataset

        value: float
            New value for the update
        """
        new_bag = self.get_bag(bag)
        new_bag.set_attribute(index_instance, attribute, value)
        self.data[new_bag.key] = new_bag

    def add_attribute(self, position: int, values=None) -> None:
        """
        Add attribute to the dataset

        Parameters
        ----------
        position : int
            Index for the new attribute

        values:  ndarray of shape(n_instances)
            Values for the new attribute
        """
        # TODO: Arreglar
        for bag_index, bag in enumerate(self.data.keys()):
            add_values = values[bag_index]
            if values is None:
                add_values = np.zeros(self.data[bag].get_number_instances())
            self.data[bag].add_attribute(position, add_values)

    def delete_attribute(self, position: int) -> None:

        """
        Delete attribute of the dataset

        Parameters
        ----------
        position : int
            Index of the attribute to be deleted
        """
        for bag in self.data.keys():
            self.data[bag].data = np.delete(self.data[bag].data, position, axis=1)
        self.attributes.pop(list(self.attributes)[position])

    def show_dataset(self, mode: str="table", head: int = None, attributes=None, labels=None, info=True) -> None:
        """
        Function to show information about the dataset

        Parameters
        ----------
            head : int
                Number of the nth firsts bag to show

            attributes: List of string
                Attributes to show

            labels : List of string
                Labels to show

            info: Boolean
                Show more info
        """
        # TODO: Hacer algo como head y tail de pandas, ponerlo como parametro quizas, tambien lista atributos y labels
        #  a mostrar opcionales
        if info:
            print("Name: ", self.get_name())
            print("Features: ", self.get_features_name())
            print("Labels: ", self.get_labels_name())
            print("Bags:")

        if mode == "table":
            for bag_index in range(self.get_number_bags()):
                bag = self.get_bag(bag_index)
                bag.show_bag()
                if head is not None:
                    if bag_index+1 >= head:
                        break

        elif mode == "compact":
            header = [self.name] + self.get_features_name() + self.get_labels_name()
            print(", ".join(header))
            for bag_index in range(self.get_number_bags()):
                bag = self.get_bag(bag_index)
                for index_instance in range(bag.get_number_instances()):
                    print(", ".join([bag.key] + list(bag.get_instance(index_instance).get_attributes())))

                if head is not None:
                    if bag_index+1 >= head:
                        break

        else:
            raise Exception("Mode not available. Mode options are \"table\" and \"compact\"")

    def split_dataset(self, train_percentage: float=0.8, seed=0):
        for count_label in np.sum(self.get_features_by_bag(), 1):
            print(count_label)
            if count_label == 0:
                raise Exception("Dataset contain a label with no positive instance for a label")

        random.seed(seed)
        labels_train = [range(self.get_number_labels())]
        bags_not_used = [range(self.get_number_bags())]

        dataset_train = MIMLDataset()
        dataset_train.set_name(self.get_name()+"_train")
        dataset_train.set_features_name(self.get_features_name())
        dataset_train.set_labels_name(self.get_labels_name())

        dataset_test = MIMLDataset()
        dataset_test.set_name(self.get_name() + "_test")
        dataset_test.set_features_name(self.get_features_name())
        dataset_test.set_labels_name(self.get_labels_name())

        while bags_not_used and labels_train:
            bag_index = random.randint(0, len(bags_not_used)-1)
            bag = self.get_bag(bags_not_used[bag_index])
            used = False

            for label_index in range(len(bag.get_labels())):
                if bag.get_labels()[label_index] == 1 and label_index in labels_train:
                    used = True
                    del labels_train[label_index]
            if used:
                del bags_not_used[bag_index]






    # TODO: Ver si separar esto
    def cardinality(self):
        """
        Computes the Cardinality as the average number of labels per pattern.

        Returns
        ----------
        cardinality : float
            Average number of labels per pattern
        """
        suma = 0
        for key in self.data:
            suma += sum(self.get_bag(key).get_labels()[0])
        return suma / self.get_number_bags()

    def density(self):
        """
        Computes the density as the cardinality / numLabels.

        Returns
        ----------
        density : float
            Cardinality divided by number of labels
        """
        return self.cardinality() / self.get_number_labels()

    def distinct(self):
        """
        Computes the numbers of labels combinations used in the dataset respect all the possible ones

        Returns
        -------
        distinct : float
            Numbers of labels combinations used in the dataset divided by all possible combinations
        """
        options = set()
        for key in self.data:
            options.add(tuple(self.get_bag(key).get_labels()[0]))
        return len(options) / (2 ** self.get_number_labels())

    def get_statistics(self):
        """
        Calculate statistics of the dataset

        Returns
        -------
        n_instances : int
            Numbers of instances of the dataset

        min_instances : int
            Number of instances in the bag with minimum number of instances

        max_instances : int
            Number of instances in the bag with maximum number of instances

        distribution : dict
            Distribution of number of instances in bags
        """
        n_instances = self.get_number_instances()
        max_instances = 0
        min_instances = float("inf")
        distribution = dict()
        for key in self.data:
            instances_bag = self.get_bag(key).get_number_instances()
            if instances_bag in distribution:
                distribution[instances_bag] += 1
            else:
                distribution[instances_bag] = 1
            if instances_bag < min_instances:
                min_instances = instances_bag
            if instances_bag > max_instances:
                max_instances = instances_bag
        return n_instances, min_instances, max_instances, distribution

    def describe(self):
        """
        Print statistics about the dataset
        """

        print("-----MULTILABEL-----")
        print("Cardinality: ", self.cardinality())
        print("Density: ", self.density())
        print("Distinct: ", self.distinct())
        print("")
        n_instances, min_instances, max_instances, distribution = self.get_statistics()
        print("-----MULTIINSTANCE-----")
        print("Nº of bags: ", self.get_number_bags())
        print("Total instances: ", n_instances)
        print("Average Instances per bag: ", n_instances / self.get_number_bags())
        print("Min Instances per bag: ", min_instances)
        print("Max Instances per bag: ", max_instances)
        print("Attributes per bag: ", self.get_number_attributes())
        print("\nDistribution of bags:")
        for number_instances_in_bag, occurrences in sorted(distribution.items()):
            print("\tBags with ", number_instances_in_bag, " instances: ", occurrences)
