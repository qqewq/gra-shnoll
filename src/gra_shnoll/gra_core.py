"""Ядро ГРА Мета-обнулёнки: проекторы, функционал пены, обновление состояния."""

import numpy as np

class GRAState:
    def __init__(self, dim: int, levels: int = 3, alpha: float = 0.7):
        self.dim = dim
        self.levels = levels
        self.alpha = alpha
        self.lambda_0 = 1.0
        self.psi = [np.random.randn(dim) + 1j * np.random.randn(dim) for _ in range(levels)]
        self.projectors = [np.eye(dim) for _ in range(levels)]
        self.foam_history = [[] for _ in range(levels)]

    def compute_projectors(self, constraints: list):
        """Инициализирует проекторы из ограничений (упрощённо)."""
        for l, cons in enumerate(constraints):
            P = np.eye(self.dim)
            if cons == 'sensor_agreement':
                P[:3, :3] *= 0.8
            elif cons == 'ephemeris_consistency':
                P[3:6, 3:6] *= 0.6
            elif cons == 'mission_feasibility':
                P[6:, 6:] *= 0.4
            self.projectors[l] = P

def foam_functional(psi_list: list, projectors: list) -> float:
    """Φ⁽ˡ⁾ = Σ_{a≠b} |⟨Ψ⁽ᵃ⁾|𝒫_G_l|Ψ⁽ᵇ⁾⟩|² (векторизованная оценка)"""
    foam = 0.0
    for psi, P in zip(psi_list, projectors):
        proj = P @ psi
        foam += np.sum(np.abs(proj)**2) * (1 - np.abs(np.vdot(psi, proj)) / np.linalg.norm(psi)**2)
    return foam

def update_gra_state(gras: GRAState, foam_grad: np.ndarray, eta: float = 1e-3, D: float = 0.5):
    """Ψ ← Ψ - η∇J_GRA + √(2ηD)·ξ(t)"""
    for l in range(gras.levels):
        noise = eta * (np.random.randn(gras.dim) + 1j * np.random.randn(gras.dim))
        gras.psi[l] -= eta * foam_grad[l] + noise
        gras.psi[l] /= (np.linalg.norm(gras.psi[l]) + 1e-12)
        gras.foam_history[l].append(foam_functional([gras.psi[l]], [gras.projectors[l]]))
