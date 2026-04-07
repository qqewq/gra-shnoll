"""Модуль расчёта космофизического вектора X_cosmo(t)."""

import numpy as np
from astropy.time import Time
from astropy.coordinates import EarthLocation, get_body_barycentric
import warnings

def _sinusoidal_approx(t_utc: np.ndarray, lat: float = 55.7, lon: float = 37.6, alt: float = 150.0) -> np.ndarray:
    """Упрощённая аппроксимация для оффлайн-тестов."""
    t_sec = (t_utc - t_utc[0]) / 86400.0
    solar = np.sin(2 * np.pi * t_sec)
    lunar = np.sin(2 * np.pi * t_sec / 27.32)
    g_vec = np.array([
        9.81 + 0.001 * solar + 0.0003 * lunar,
        0.002 * np.cos(2 * np.pi * t_sec),
        0.002 * np.sin(2 * np.pi * t_sec / 27.32),
        0.46 * np.cos(np.radians(lat)) * np.cos(2 * np.pi * t_sec),  # v_lab_x
        0.46 * np.cos(np.radians(lat)) * np.sin(2 * np.pi * t_sec),  # v_lab_y
        alt / 6371.0  # нормализованная высота
    ])
    return np.tile(g_vec[:, None], (1, len(t_sec))).T

def compute_cosmophysical_vector(t_utc, lat=55.7, lon=37.6, alt=150.0, use_real=True):
    """Вычисляет X_cosmo = [g_☉, g_☾, B_earth, v_lab, alt_norm]."""
    if not use_real:
        return _sinusoidal_approx(t_utc, lat, lon, alt)

    try:
        loc = EarthLocation(lat=lat, lon=lon, height=alt)
        t_ast = Time(t_utc, format='unix')
        sun = get_body_barycentric('sun', t_ast)
        moon = get_body_barycentric('moon', t_ast)

        g_sun = sun.distance.value / 1e9
        g_moon = moon.distance.value / 1e9
        v_lab = loc.get_gcrs().velocity.norm().value

        return np.column_stack([
            np.full_like(t_utc, g_sun),
            np.full_like(t_utc, g_moon),
            np.full_like(t_utc, 0.0),  # B_earth placeholder (требует IGRF)
            v_lab * np.ones_like(t_utc),
            alt / 6371.0 * np.ones_like(t_utc)
        ])
    except Exception as e:
        warnings.warn(f"Ephemeris fallback: {e}")
        return _sinusoidal_approx(t_utc, lat, lon, alt)
