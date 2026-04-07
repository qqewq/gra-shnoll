"""Навигационный фильтр частиц с Мастер-формулой ГРА-Шноль."""

import numpy as np
from scipy.stats import poisson
from .p_adic import modulation_factor
from .cosmophysics import compute_cosmophysical_vector
from .gra_core import GRAState, update_gra_state

class GRA_Shnoll_Navigator:
    def __init__(self, config: dict):
        self.N = config['navigation']['particle_count']
        self.lambda_0 = config['navigation']['lambda_base']
        self.primes = config['p_adic']['primes']
        self.k_vec = np.array([1.0, 0.5, 0.2, 0.1, 0.05])
        self.c_p = np.ones(len(self.primes)) / len(self.primes)
        self.gra = GRAState(dim=10, levels=config['gra']['levels'], alpha=config['gra']['alpha'])
        self.gra.compute_projectors(['sensor_agreement', 'ephemeris_consistency', 'mission_feasibility'])
        self.eta = config['gra']['eta']
        self.D = config['gra']['D']
        self.gamma = config['navigation']['gamma_gra']

    def master_formula_weight(self, n: int, t: float, X: np.ndarray, r_candidate: np.ndarray) -> float:
        """P(n|r,t) = Pois(λ) · |Σ...|² · |⟨Ψ|𝒫_G|n⟩|²"""
        pois = poisson.pmf(n, self.lambda_0)
        mod = modulation_factor(np.array([n]), t, X, self.primes, self.k_vec, self.c_p)[0]
        gra_proj = np.mean([np.abs(np.vdot(self.gra.psi[l], np.random.randn(10) + 1j*np.random.randn(10)))**2 
                            for l in range(self.gra.levels)])
        return pois * mod * (1 + self.gamma * gra_proj)

    def estimate_position(self, histogram: np.ndarray, t_utc: float, 
                          lat: float, lon: float, alt: float) -> dict:
        """Один шаг навигации: фильтр частиц + обновление ГРА."""
        X = compute_cosmophysical_vector(np.array([t_utc]), lat, lon, alt)[0]
        candidates = np.random.multivariate_normal(
            mean=[lat, lon, alt], cov=np.diag([0.001, 0.001, 1.0]), size=self.N)

        weights = np.array([
            self.master_formula_weight(histogram[0], t_utc, X, c) for c in candidates
        ])
        weights /= np.sum(weights) + 1e-15

        pos_est = np.average(candidates, weights=weights, axis=0)
        cov_est = np.cov(candidates.T, aweights=weights)

        # Обновление ГРА
        grad_approx = [np.random.randn(10) for _ in range(self.gra.levels)]
        update_gra_state(self.gra, grad_approx, self.eta, self.D)

        return {
            'position': pos_est,
            'covariance': cov_est,
            'effective_samples': 1.0 / np.sum(weights**2),
            'X_cosmo': X,
            'weights': weights
        }
