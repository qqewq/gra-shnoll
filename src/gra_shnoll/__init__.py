"""GRA-Shnoll: Космофизическая навигация на основе стохастического резонанса."""

__version__ = "1.0.0"
__author__ = "Oleg Bit"

from .p_adic import p_adic_weight, phase_theta, modulation_factor
from .cosmophysics import compute_cosmophysical_vector
from .gra_core import GRAState, foam_functional, update_gra_state
from .navigation import GRA_Shnoll_Navigator
from .utils import build_histogram, normalize, plot_results

__all__ = [
    "p_adic_weight", "phase_theta", "modulation_factor",
    "compute_cosmophysical_vector", "GRAState", "foam_functional",
    "update_gra_state", "GRA_Shnoll_Navigator", "build_histogram",
    "normalize", "plot_results"
]
