from sklearn.model_selection import train_test_split
from wrangler import Wrangler
from sklearn import preprocessing
from sklearn.utils import shuffle
from operator import itemgetter
from sklearn import datasets
import pandas as pd
import numpy as np

class Shell:
    def __init__(self, data, target, classifier, filename=None):
        if data is not None:
            self.data = data
        elif filename[:3] == 'csv':
            self.data = pd.read_csv(filename)
        elif filename[:3] == 'txt':
            self.data = pd.DataFrame(filename)
        else:
            print("Data Invalid")

        self.target = target

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.data,
                                                                                self.target,
                                                                                test_size=0.7,
                                                                                train_size=0.3)
        self.classifier = classifier

    def shuffle_data(self):
        df_data = pd.DataFrame(self.data)
        df_target = pd.DataFrame(self.target)
        df_merged = pd.concat([df_data, df_target], axis=1)
        df_merged = shuffle(df_merged)
        self.data = df_merged.iloc[:,0:-1].as_matrix()
        self.target = df_merged.iloc[:,-1].as_matrix()

    def fit_model_to_shell(self):
        """fit the model on the data provided for the shell"""
        self.model = self.classifier.fit(self.x_train, self.y_train)


    def predict_from_classifier(self):
        """predict from the classifier and store them in the shell as y_predicted"""
        self.y_predicted = self.model.predict(self.x_test)

    def cross_val_custom(self, k=2, _range=0):
        accuracies = []

        # shuffle data
        self.shuffle_data()
        # find bin size
        size = self.data.shape[0]
        bin_size = int(size / k)

        # cut the frame into bins, grab one for test, k - 1 for train
        for x in range(k):
            print(f"Cross val #{x + 1}...")
            indexes = [range((0 + (x * bin_size)), bin_size + (x * bin_size))]

            self.x_test = pd.DataFrame(self.data[indexes])
            self.x_train = pd.DataFrame(np.delete(self.data, indexes, axis=0))
            self.y_test = pd.DataFrame(self.target[indexes])
            self.y_train = pd.DataFrame(np.delete(self.target, indexes, axis=0))

            # run the normal methods
            self.fit_model_to_shell()
            self.predict_from_classifier()

            # put accuracy in list
            accuracies.append(self.get_accuracy(_range))
        print(accuracies)
        accuracies = np.array(accuracies)
        print(f"Mean accuracy is {round(np.mean(accuracies), 1)}%")

    def eval_range(self, _range, x):
        return ((self.y_test[x] + _range <= self.y_predicted[x]) or
                (self.y_test[x] - _range >= self.y_predicted[x]))

    def get_accuracy(self, _range=0):
        correct = 0
        for x in range(len(self.y_test)):
            if not isinstance(self.y_test, np.ndarray):
                test = self.y_test.values.tolist()[x]
            else:
                test = self.y_test[x]
            # print(f"Target: {self.y_test.values.tolist()[x]} ---- > {self.y_predicted[x]}")
            if test == self.y_predicted[x]:
                correct += 1
        accuracy = (correct / float(len(self.y_test))) * 100.0
        return round(accuracy, 1)


# w = Wrangler()

""" our implementation of iris """
# iris_shell = Shell(w.iris.data,
#                    w.iris.targets,
#                    NeuralNetClassifier(hidden_layers_info=[5,4],
#                                        learn_rate=0.2,
#                                        epochs=200,
#                                        thres_function='sigmoid')
#                   )
#
# iris_shell.fit_model_to_shell()
# iris_shell.predict_from_classifier()
# print(f"Accuracy: {iris_shell.get_accuracy()}%")
