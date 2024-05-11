from dtm_nn.activation_relu import ReLU


class TestReLU:

    def test_relu_function(self):
        # Assert
        assert 2 == ReLU.fn(2)
        assert 1 == ReLU.fn(1)
        assert 0 == ReLU.fn(-1)

    def test_relu_derivative(self):
        assert 1 == ReLU.derivative(2)
        assert 0 == ReLU.derivative(0)
        assert 0 == ReLU.derivative(-1)
