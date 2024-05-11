import numpy as np


class SoftMax:
    @staticmethod
    def fn(z):
        """The SoftMax function calculates the probabilities of given
        matrix along axis 1.

        exp: Elementwise e^(element) is divided by
        sigma: Sum of Elementwise e^(element)
        """

        exp = np.exp(z)
        sigma = np.sum(exp, axis=1, keepdims=True)
        return exp / sigma

    @staticmethod
    def derivative(z):
        """
        Derivative of the SoftMax function.
        """
        pass
