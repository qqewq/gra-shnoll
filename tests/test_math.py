import numpy as np
import pytest
from gra_shnoll.p_adic import digit_sum_base_p, p_adic_weight, modulation_factor
from gra_shnoll.gra_core import GRAState, foam_functional

def test_digit_sum():
    assert digit_sum_base_p(100, 10) == 1
    assert digit_sum_base_p(100, 100) == 1
    assert digit_sum_base_p(15, 2) == 4  # 1111₂

def test_p_adic_weight():
    w = p_adic_weight(10, 101, 1.0/3)
    assert 0 < w < 1.0

def test_modulation_factor():
    counts = np.arange(50, 150)
    t, X, k, p, c = 86400.0, np.zeros(5), np.ones(5), [97], np.array([1.0])
    mod = modulation_factor(counts, t, X, p, k, c)
    assert np.all(mod >= 0)
    assert np.max(mod) > 0

def test_gra_foam():
    gras = GRAState(dim=5, levels=2)
    foam = foam_functional(gras.psi, gras.projectors)
    assert isinstance(foam, float)
    assert foam >= 0
