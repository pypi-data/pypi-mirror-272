import numpy as np


class Accuracy:

    @staticmethod
    def accuracy(y_true, y_pred):
        """
        Accepts one dimensional array of tru and predicted labels.

        Accuracy.accuracy(np.array([0.0, 1.0, 2.0]), np.array([1.0, 0.0, 2.0]))
        >>> np.array(0.333333)
        """
        return np.mean(y_pred == y_true)
