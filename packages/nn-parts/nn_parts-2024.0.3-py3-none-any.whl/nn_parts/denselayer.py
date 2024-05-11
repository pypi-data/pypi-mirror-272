import random

import numpy as np


class DenseLayer:
    """Class Network creates neural neural_network

    The list ``sizes`` contains the number of neurons in the
    respective layers of the neural_network.
    For example, if the list was [2, 3, 1] then it would be a
    three-layer neural_network, with the first layer containing 2 neurons,
    the second layer 3 neurons, and the third layer 1 neuron.
    """

    def __init__(self, n_inputs=0, n_neurons=0):
        self._weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self._biases = np.zeros((1, n_neurons))

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, weights):
        self._weights = weights

    @property
    def biases(self):
        return self._biases

    @biases.setter
    def biases(self, biases):
        self._biases = biases

    def feedforward(self, inputs=None):
        """Calculate (wx+b) for one layer only."""
        return np.dot(inputs, self.weights) + self.biases
