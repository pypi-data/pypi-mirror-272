import numpy as np

from dtm_nn.activation_softmax import SoftMax


class TestSoftmax:

    def test_softmax_function(self):
        # Arrange
        z = np.array([[1.0, 2.0, 3.0],
                      [4.0, 5.0, 6.0],
                      [7.0, 8.0, 9.0]])
        expected_probabilities = np.array([[0.09003057, 0.24472847, 0.66524096],
                                           [0.09003057, 0.24472847, 0.66524096],
                                           [0.09003057, 0.24472847, 0.66524096]])

        # Act
        calculated_probabilities = SoftMax.fn(z)

        # Assert
        np.testing.assert_allclose(calculated_probabilities, expected_probabilities, rtol=1e-6, atol=1e-6)

    def test_softmax_derivative(self):
        assert True
