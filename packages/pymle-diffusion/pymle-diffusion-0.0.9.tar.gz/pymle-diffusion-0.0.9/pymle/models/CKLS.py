from typing import Union
import numpy as np

from pymle.core.Model import Model1D


class CKLS(Model1D):
    """
    Model for CKLS
    Parameters: [theta_1, theta_2, theta_3, theta_4]

    dX(t) = mu(X,t)*dt + sigma(X,t)*dW_t

    where:
        mu(X,t)    = (theta_1 + theta_2*X)
        sigma(X,t) = theta_3 * X^(theta_4)
    """

    def __init__(self):
        super().__init__()

    def drift(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return self._params[0] + self._params[1] * x

    def diffusion(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return self._params[2] * x ** self._params[3]

    # =======================
    # (Optional) Overrides for numerical derivatives to improve performance
    # =======================

    def drift_t(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return 0.

    def _set_is_positive(self, params: np.ndarray) -> bool:
        return params[0] > 0 and params[1] > 0 and params[3] > 0.5

    def AitSahalia_density(self, x0: float, xt: float, t0: float, dt: float) -> float:

        #am1, a0, a1, a2, b0, b1, b2, b3 = self._params
        theta1, theta2, theta3, theta4 = self._params


        x = xt

        dell = dt

        am1 = 0
        a0 = theta1
        a1 = theta2
        a2 = 0

        b0 = 0
        b1 = 0
        b2 = theta3
        b3 = theta4



        sx = b0 + b1 * x + b2 * x ** b3
        cm1 = -((x - x0) ** 2 / (2 * (b0 + b1 * x0 + b2 * x0 ** b3) ** 2)) + (
                    (x - x0) ** 3 * (b1 + b2 * b3 * x0 ** (-1 + b3))) / (2 * (b0 + b1 * x0 + b2 * x0 ** b3) ** 3) + \
              ((x - x0) ** 4 * (
                          -11 * (b1 + b2 * b3 * x0 ** (-1 + b3)) ** 2 + 4 * b2 * (-1 + b3) * b3 * x0 ** (-2 + b3) *
                          (b0 + b1 * x0 + b2 * x0 ** b3))) / (24 * (b0 + b1 * x0 + b2 * x0 ** b3) ** 4)

        c0 = ((x - x0) * ((-(b1 + b2 * b3 * x0 ** (-1 + b3))) * (b0 + b1 * x0 + b2 * x0 ** b3) + 2 *
                          (a0 + am1 / x0 + x0 * (a1 + a2 * x0)))) / (2 * (b0 + b1 * x0 + b2 * x0 ** b3) ** 2) + (
                         (x - x0) ** 2 *
                         ((-b2) * (-1 + b3) * b3 * x0 ** (-2 + b3) * (b0 + b1 * x0 + b2 * x0 ** b3) ** 2 - 4 *
                          (b1 + b2 * b3 * x0 ** (-1 + b3)) * (a0 + am1 / x0 + x0 * (a1 + a2 * x0)) +
                          (b0 + b1 * x0 + b2 * x0 ** b3) * (2 * (a1 - am1 / x0 ** 2 + 2 * a2 * x0) +
                                                            (b1 + b2 * b3 * x0 ** (-1 + b3)) ** 2))) / (
                         4 * (b0 + b1 * x0 + b2 * x0 ** b3) ** 3)

        c1 = (-(1 / (8 * (b0 + b1 * x0 + b2 * x0 ** b3) ** 2))) * (
                    -8 * (b1 + b2 * b3 * x0 ** (-1 + b3)) * (b0 + b1 * x0 + b2 * x0 ** b3) *
                    (a0 + am1 / x0 + x0 * (a1 + a2 * x0)) + 4 * (a0 + am1 / x0 + x0 * (a1 + a2 * x0)) ** 2 +
                    (b0 + b1 * x0 + b2 * x0 ** b3) ** 2 * (
                                4 * (a1 - am1 / x0 ** 2 + 2 * a2 * x0) + (b1 + b2 * b3 * x0 ** (-1 + b3)) ** 2 -
                                2 * b2 * (-1 + b3) * b3 * x0 ** (-2 + b3) * (b0 + b1 * x0 + b2 * x0 ** b3)))

        output = -(1 / 2) * np.log(2 * np.pi * dell) - np.log(sx) + cm1 / dell + c0 + c1 * dell

        return np.exp(output)

