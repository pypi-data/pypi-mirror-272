from typing import Union
import numpy as np
from scipy.stats import norm
from pymle.core.Model import Model1D


class BrownianMotion(Model1D):
    """
    Model for (drifted) Brownian Motion
    Parameters:  [mu, sigma]

    dX(t) = mu(X,t)dt + sigma(X,t)dW_t

    where:
        mu(X,t)    = mu   (constant)
        sigma(X,t) = sigma   (constant, >0)
    """

    def __init__(self):
        super().__init__(has_exact_density=True, default_sim_method='Exact', has_constant_diffusion=True)

    def drift(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return self._params[0] * (x > -10000)  # todo: reshape?

    def diffusion(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return self._params[1] * (x > -10000)

    def exact_density(self, x0: float, xt: float, t0: float, dt: float) -> float:
        mu, sigma = self._params
        mean_ = x0 + mu * dt
        return norm.pdf(xt, loc=mean_, scale=sigma * np.sqrt(dt))

    def exact_step(self,
                   t: float,
                   dt: float,
                   x: Union[float, np.ndarray],
                   dZ: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """ Simple Brownian motion can be simulated exactly """
        sig_sq_dt = self._params[1] * np.sqrt(dt)
        return x + self._params[0] * dt + sig_sq_dt * dZ

    # =======================
    # (Optional) Overrides for numerical derivatives to improve performance
    # =======================

    def drift_t(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return 0.

    def diffusion_x(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return 0.

    def diffusion_xx(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return 0.

    def AitSahalia_density(self, x0: float, xt: float, t0: float, dt: float) -> float:

        mu, sigma = self._params
        x = xt
        dell = dt

        a = mu
        b = 0
        c = 0
        d = 0
        f = sigma

        sx = f

        cm1 = -(x - x0)**2 / (2 * f**2)

        c0 = (4 * c * x**3 + 3 * d * x**4 + 12 * a * (x - x0) - 4 * c * x0**3 - 3 * d * x0**4 + 6 * b * (
                    x**2 - x0**2)) / (12 * f**2)

        c1 = -1 / (420 * f**2) * (210 * a**2 + 70 * b**2 * (x**2 + x * x0 + x0**2) +
                35 * a * (6 * b * (x + x0) + 4 * c * (x**2 + x * x0 + x0**2) +
                 3 * d * (x**3 + x**2 * x0 + x * x0**2 + x0**3)) +
                 21 * b * (10 * f**2 + 5 * c * (x**3 + x**2 * x0 + x * x0**2 + x0**3) +
                 4 * d * (x**4 + x**3 * x0 + x**2 * x0**2 + x * x0**3 + x0**4)) +
                 2 * (21 * c**2 * (x**4 + x**3 * x0 + x**2 * x0**2 + x * x0**3 + x0**4) +
                 35 * c * (x + x0) * (3 * f**2 + d * (x**4 + x**2 * x0**2 + x0**4)) +
                 15 * d * (7 * f**2 * (x**2 + x * x0 + x0**2) +
                 d * (x**6 + x**5 * x0 + x**4 * x0**2 + x**3 * x0**3 + x**2 * x0**4 + x * x0**5 +
                 x0**6))))

        c2 = 1 / 210 * (
                    -35 * b ** 2 - 105 * d * f ** 2 - 63 * c ** 2 * x ** 2 - 140 * c * d * x ** 3 - 75 * d ** 2 * x ** 4 -
                    84 * c ** 2 * x * x0 - 210 * c * d * x ** 2 * x0 - 120 * d ** 2 * x ** 3 * x0 - 63 * c ** 2 * x0 ** 2 -
                    210 * c * d * x * x0 ** 2 - 135 * d ** 2 * x ** 2 * x0 ** 2 - 140 * c * d * x0 ** 3 - 120 * d ** 2 * x * x0 ** 3 -
                    75 * d ** 2 * x0 ** 4 - 35 * a * (2 * c + 3 * d * (x + x0)) -
        21 * b * (5 * c * (x + x0) + 2 * d * (3 * x ** 2 + 4 * x * x0 + 3 * x0 ** 2)))

        output = -np.log(2 * np.pi*dell)/2 - np.log(sx) + cm1 /dell + c0 + c1 *dell + c2 *dell**2 / 2

        return np.exp(output)
