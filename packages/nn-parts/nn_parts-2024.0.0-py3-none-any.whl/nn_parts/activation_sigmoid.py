import numpy as np


class Sigmoid:

    @staticmethod
    def fn(z):
        """The sigmoid function."""
        return 1.0 / (1.0 + np.exp(-z))

    @staticmethod
    def derivative(z):
        """
        Derivative of the sigmoid function.
        """
        return Sigmoid.fn(z) * (1 - Sigmoid.fn(z))