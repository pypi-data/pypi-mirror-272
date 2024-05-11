import numpy as np

from dtm_nn.cost_cross_entropy import CrossEntropy


class TestCrossEntropy:

    def test_cross_entropy_cost_function(self):
        # Arrange
        y_hat = np.array([[[0.19003057, 0.24472847, 0.56524096],  # Normal case
                           [0.19003057, 0.24472847, 0.56524096],
                           [0.0, 1.0, 0.0],  # Correct prediction
                           [0.0, 0.0, 0.0]  # y and y_hat all 0
                           ]])  # Both 0
        y = np.array([[0.0, 0.0, 1.0],
                      [0.0, 1.0, 0.0],
                      [0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0]
                      ])

        expected_cost = np.array(3.513268)

        # Act
        cost = CrossEntropy.fn(y, y_hat)

        # Assert
        np.testing.assert_allclose(expected_cost, cost, rtol=1e-6, atol=1e-6)

    def test_cross_entropy_cost_function_infinity_value(self):
        # Arrange
        y_hat = np.array([[[0.19003057, 0.24472847, 0.56524096],  # Normal case
                           [1.0, 0.0, 0.0],  # Wrong prediction
                           [0.0, 1.0, 0.0],  # Double label
                           [0.0, 1.0, 0.0],  # Correct prediction
                           [0.0, 1.0, 0.0],  # y is all 0
                           [0.0, 0.0, 0.0]]])  # Both 0
        y = np.array([[0.0, 0.0, 1.0],
                      [0.0, 1.0, 0.0],
                      [0.0, 1.0, 0.5],
                      [0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0]])

        expected_cost = np.array(351.06194)

        # Act
        cost = CrossEntropy.fn(y, y_hat)

        # Assert
        np.testing.assert_allclose(expected_cost, cost, rtol=1e-6, atol=1e-6)

    def test_cross_entropy_delta(self):
        # Arrange
        y_hat = np.array([[[0.19003057, 0.24472847, 0.56524096],
                           [0.29003057, 0.24472847, 0.46524096],
                           [0.39003057, 0.24472847, 0.36524096]]])
        y = np.array([[0.09003057, 0.24472847, 0.66524096],
                      [0.09003057, 0.24472847, 0.66524096],
                      [0.09003057, 0.24472847, 0.66524096]])

        expected_cost = np.array([[[0.1, 0., -0.1],
                                   [0.2, 0., -0.2],
                                   [0.3, 0., -0.3]]])

        # Act
        cost = CrossEntropy.delta(y, y_hat)

        # Assert
        np.testing.assert_allclose(-expected_cost, cost, rtol=1e-6, atol=1e-6)
