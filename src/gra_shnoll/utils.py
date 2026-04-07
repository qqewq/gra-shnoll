"""Утилиты: гистограммы, нормализация, визуализация."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def build_histogram(counts: list, window: int = 6000) -> np.ndarray:
    """Строит скользящую гистограмму с заданным окном."""
    if len(counts) < window:
        return np.array([counts])
    return np.histogram(counts[-window:], bins=range(max(counts[-window:])+2))[0]

def normalize(arr: np.ndarray) -> np.ndarray:
    s = np.sum(arr)
    return arr / s if s > 0 else arr

def plot_results(history: dict, save_path: str = 'output/navigation.png'):
    """Визуализация траектории, гистограммы и сходимости ГРА."""
    import os
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    pos = np.array(history['positions'])
    axes[0, 0].plot(pos[:, 0], pos[:, 1], '-o', markersize=3)
    axes[0, 0].set_title('Траектория (lat, lon)')
    axes[0, 0].grid()

    axes[0, 1].bar(range(len(history['histograms'][-1])), normalize(history['histograms'][-1]))
    axes[0, 1].set_title('Гистограмма счётов (последняя)')

    axes[1, 0].plot(history['effective_samples'])
    axes[1, 0].set_title('Effective Samples (N_eff)')
    axes[1, 0].set_yscale('log')

    axes[1, 1].plot(history['gra_foam'])
    axes[1, 1].set_title('Функционал пены Φ⁽ˡ⁾')

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"✅ Результат сохранён: {save_path}")
