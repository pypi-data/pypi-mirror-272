import numpy as np


class Quadratic(object):

    @staticmethod
    def fn(y, y_hat):
        """Return the cost associated with an output ``a`` and desired output
        ``y``.

        """
        return 0.5 * np.linalg.norm(y - y_hat) ** 2

    @staticmethod
    def delta(y, y_hat):
        """Return the error delta from the output layer."""
        return y - y_hat
