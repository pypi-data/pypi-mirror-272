import numpy as np


class CrossEntropy:
    @staticmethod
    def fn(y, y_hat, low_val_en=100):
        """Return the cost associated with an output ``a`` and desired output
        ``y``.  Note that np.nan_to_num is used to ensure numerical
        stability.  In particular, if both ``a`` and ``y`` have a 1.0
        in the same slot, then the expression (1-y)*np.log(1-a)
        returns nan.  The np.nan_to_num ensures that that is converted
        to the correct value (0.0).

        """
        one_minus_y_hat = 1 - y_hat

        return np.sum(np.nan_to_num(
            -y * np.log(y_hat, where=y_hat > 0, out=(0 * y_hat - low_val_en))
            - (1 - y) * np.log(one_minus_y_hat, where=one_minus_y_hat > 0, out=(0 * one_minus_y_hat - low_val_en))))

    @staticmethod
    def delta(y, y_hat):
        """Return the error delta from the output layer.  Note that the
        parameter ``z`` is not used by the method.  It is included in
        the method's parameters in order to make the interface
        consistent with the delta method for other cost classes.

        """
        return y - y_hat
