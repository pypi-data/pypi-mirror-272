import json

import numpy as np

from dtm_nn.denselayer import DenseLayer


class TestDenseLayer:

    def test_feedforward(self):
        # Arrange
        with open("./data/dense_layer.json") as f:
            data = json.load(f)

        net = DenseLayer(4, 3)
        net.weights = np.array(data['weights'])
        net.biases = np.array(data['biases'])
        layer_1_output = np.array(data['layer_1_output'])

        # Act
        prediction = net.feedforward(np.array(data['inputs']))

        # Assert
        np.testing.assert_allclose(prediction, layer_1_output, rtol=1e-6, atol=1e-6)
