from dtm_nn.activation_sigmoid import Sigmoid


class TestSigmoid:

    def test_sigmoid_function(self):
        # Assert
        assert 0.8807970779778823 == Sigmoid.fn(2)

    def test_sigmoid_derivative(self):
        assert 0.10499358540350662 == Sigmoid.derivative(2)
