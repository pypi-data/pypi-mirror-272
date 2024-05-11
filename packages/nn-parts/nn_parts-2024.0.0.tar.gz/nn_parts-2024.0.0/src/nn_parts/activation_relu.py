import numpy as np


class ReLU:

    @staticmethod
    def fn(z):
        """The relu function."""
        return np.maximum(z, 0)

    @staticmethod
    def derivative(z):
        """
        Derivative of the relu function.
        """
        return 1 * (z > 0)
