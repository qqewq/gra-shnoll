"""p-адическая модуляция и фазовые вычисления."""

import numpy as np

def digit_sum_base_p(n: int, p: int) -> int:
    """Сумма цифр числа n в системе счисления по основанию p."""
    s = 0
    while n > 0:
        n, rem = divmod(n, p)
        s += rem
    return s

def phase_theta(n: int, p: int, t: float, X: np.ndarray, k_vec: np.ndarray) -> complex:
    """θ_p(n, t, X) = (2π/p)[ω·t + k·X]"""
    omega_t = 2 * np.pi * t / 86400.0  # масштаб суток
    phase_arg = (2 * np.pi / p) * (omega_t + np.dot(k_vec, X))
    return np.exp(1j * phase_arg)

def p_adic_weight(n: int, p: int, c_p: float) -> float:
    """w_p(n) = c_p · p^{-s_p(n)}"""
    return c_p * (p ** (-digit_sum_base_p(n, p)))

def modulation_factor(counts: np.ndarray, t: float, X: np.ndarray, 
                      primes: list, k_vec: np.ndarray, c_p: np.ndarray) -> np.ndarray:
    """Вычисляет |Σ c_p · p^{-s_p(n)} · e^{iθ_p}|² для массива счётов."""
    factors = np.zeros_like(counts, dtype=complex)
    for p, cp in zip(primes, c_p):
        w = np.array([p_adic_weight(n, p, cp) for n in counts])
        ph = np.array([phase_theta(n, p, t, X, k_vec) for n in counts])
        factors += w * ph
    return np.abs(factors)**2
