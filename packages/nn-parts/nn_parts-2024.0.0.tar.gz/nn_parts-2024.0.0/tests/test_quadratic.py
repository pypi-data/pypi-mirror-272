import numpy as np

from dtm_nn.cost_quadratic import Quadratic


class TestQuadratic:

    def test_quadratic_cost_function(self):
        # Arrange
        y_hat = np.array([[1.0, 2.0, 3.0],
                          [4.0, 5.0, 6.0],
                          [7.0, 8.0, 9.0]])
        y = np.array([[0.09003057, 0.24472847, 0.66524096],
                      [0.09003057, 0.24472847, 0.66524096],
                      [0.09003057, 0.24472847, 0.66524096]])

        expected_cost = np.array(126.540183)

        # Act
        cost = Quadratic.fn(y, y_hat)

        # Assert
        np.testing.assert_allclose(expected_cost, cost, rtol=1e-6, atol=1e-6)

    def test_quadratic_delta(self):
        # Arrange
        y_hat = np.array([[1.0, 2.0, 3.0],
                          [4.0, 5.0, 6.0],
                          [7.0, 8.0, 9.0]])
        y = np.array([[0.09003057, 0.24472847, 0.66524096],
                      [0.09003057, 0.24472847, 0.66524096],
                      [0.09003057, 0.24472847, 0.66524096]])

        expected_cost = np.array([[0.909969, 1.755272, 2.334759],
                                  [3.909969, 4.755272, 5.334759],
                                  [6.909969, 7.755272, 8.334759]])

        # Act
        cost = Quadratic.delta(y, y_hat)

        # Assert
        np.testing.assert_allclose(-expected_cost, cost, rtol=1e-6, atol=1e-6)
