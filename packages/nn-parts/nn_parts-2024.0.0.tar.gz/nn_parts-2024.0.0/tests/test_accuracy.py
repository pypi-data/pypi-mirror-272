import numpy as np

from dtm_nn.metric_accuracy import Accuracy


class TestAccuracy:

    def test_accuracy_one(self):
        # Arrange
        y_hat = np.array([1.0, 0.0, 2.0])
        y = np.array([0.0, 1.0, 2.0])

        expected_accuracy = np.array(0.333333)

        # Act
        accuracy = Accuracy.accuracy(y, y_hat)

        # Assert
        np.testing.assert_allclose(expected_accuracy, accuracy, rtol=1e-6, atol=1e-6)

    def test_accuracy_two(self):
        # Arrange
        y_hat = np.array([1.0, 0.0, 2.0, 0.0])
        y = np.array([0.0, 1.0, 2.0, 0.0])

        expected_accuracy = np.array(0.5)

        # Act
        accuracy = Accuracy.accuracy(y, y_hat)

        # Assert
        np.testing.assert_allclose(expected_accuracy, accuracy, rtol=1e-6, atol=1e-6)
