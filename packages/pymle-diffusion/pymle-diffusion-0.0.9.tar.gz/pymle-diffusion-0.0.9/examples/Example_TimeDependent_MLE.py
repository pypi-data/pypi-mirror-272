"""
Description: This example demonstrates how to fit an SDE. It simulates a sample path from a Cox-Ingersol-Ross (CIR)
process, and then fits several Maximum Likelihood Estimators (MLE):
1) Exact MLE,
2) Kessler's approximation
3) Ait-Sahalia's Hermite polynomial expansion
4) Euler density
5) Shoji-Ozaki Density
"""
from pymle.sim.Simulator1D import Simulator1D
from pymle.core.TransitionDensity import EulerDensity, KesslerDensity, ShojiOzakiDensity
from pymle.fit.AnalyticalMLE import AnalyticalMLE
from pymle.core.Model import Model1D
import matplotlib.pyplot as plt
from typing import Union
import numpy as np

# warning is not logged here. Perfect for clean unit test output
with np.errstate(divide='ignore'):
    np.float64(1.0) / 0.0


class BrownianMotion_SinLevel(Model1D):
    """
    Model for (drifted) Brownian Motion
    Parameters:  [kappa, theta, gamma, sigma]

    dX(t) = mu(X,t)dt + sigma(X,t)dW_t

    where:
        mu(X,t)    = kappa * (gamma * sin(t * 2*pi) - X )
        sigma(X,t) = sigma   (constant, >0)
    """
    def __init__(self):
        super().__init__(has_constant_diffusion=True)

    def drift(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return self._params[0] * (self._params[1] * np.sin(t * 2 * np.pi) - x)

    def diffusion(self, x: Union[float, np.ndarray], t: float) -> Union[float, np.ndarray]:
        return self._params[2] * (x > -np.inf)


# ===========================
# Set the true model (CIR) params, to simulate the process
# ===========================
S0 = 0.0
kappa = 2
gamma = 2
sigma = 0.5

# ===========================
# Create the true model to fit to
# ===========================
model = BrownianMotion_SinLevel()
model.params = np.array([kappa, gamma, sigma])

# ===========================
# Simulate a sample path (we will fit to this path)
# ===========================
T = 10  # num years of the sample
freq = 365  # observations per year
dt = 1. / freq
seed = 123  # random seed: set to None to get new results each time

simulator = Simulator1D(S0=S0, M=T * freq, dt=dt, model=model).set_seed(seed=seed)
sample = simulator.sim_path()

ts = np.linspace(start=0, stop=T - dt, num=T * freq)

import seaborn as sns
sns.set_style('whitegrid')

plt.plot(ts, sample[:-1])
plt.xlabel('time', fontsize=12)
plt.ylabel('process', fontsize=12)
plt.show()

# ===========================
# Fit maximum Likelihood estimators
# ===========================
# Set the parameter bounds for fitting  (kappa, gamma, sigma)
param_bounds = [(0.5, 7), (0.01, 5), (0.001, 2)]

# Choose some initial guess for params fit
guess = np.array([3, 1.5, 0.7])

# Fit using Kessler MLE
euler_est = AnalyticalMLE(sample=sample, param_bounds=param_bounds, dt=dt,
                          t0=ts,
                          density=EulerDensity(model)).estimate_params(guess)

print(f'\nEuler MLE: {euler_est} \n')

# Fit using Kessler MLE
kessler_est = AnalyticalMLE(sample=sample, param_bounds=param_bounds, dt=dt,
                            t0=ts,
                            density=KesslerDensity(model)).estimate_params(guess)

print(f'\nKessler MLE: {kessler_est} \n')

# Fit using ShojiOzaki MLE
ShojiOzakiDensity_est = AnalyticalMLE(sample=sample, param_bounds=param_bounds, dt=dt,
                                      t0=ts,
                                      density=ShojiOzakiDensity(model)).estimate_params(guess)

print(f'\nShoji-Ozaki MLE: {ShojiOzakiDensity_est} \n')
