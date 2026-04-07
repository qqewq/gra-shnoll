#!/usr/bin/env python3
"""Запуск 24-часовой симуляции навигации ГРА-Шноль."""

import yaml
import numpy as np
import os
from tqdm import tqdm
from gra_shnoll.navigation import GRA_Shnoll_Navigator
from gra_shnoll.utils import build_histogram, plot_results

def main():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'default_params.yaml')
    with open(config_path) as f:
        config = yaml.safe_load(f)

    nav = GRA_Shnoll_Navigator(config)
    hist = [np.random.poisson(config['navigation']['lambda_base']) for _ in range(1000)]

    start_time = 1700000000.0  # ~2023-11
    history = {'positions': [], 'histograms': [], 'effective_samples': [], 'gra_foam': []}

    print("🚀 Запуск симуляции ГРА-Шноль...")
    for hour in tqdm(range(24)):
        t = start_time + hour * 3600.0
        # Имитация полёта по спирали
        lat = 55.7 + 0.01 * np.sin(hour * 0.5)
        lon = 37.6 + 0.01 * np.cos(hour * 0.5)
        alt = 150 + 50 * np.sin(hour * 0.2)

        hist.extend(np.random.poisson(config['navigation']['lambda_base'], 250))
        window_hist = build_histogram(hist, config['navigation']['histogram_window'])

        res = nav.estimate_position(window_hist, t, lat, lon, alt)
        history['positions'].append(res['position'])
        history['histograms'].append(window_hist)
        history['effective_samples'].append(res['effective_samples'])
        history['gra_foam'].append(sum(nav.gra.foam_history[l][-1] if nav.gra.foam_history[l] else 0 
                                       for l in range(nav.gra.levels)))

        if res['effective_samples'] < 100:
            print("⚠️ Перевыборка частиц (N_eff < 100)")

    os.makedirs('output', exist_ok=True)
    np.save('output/sim_results.npy', history)
    plot_results(history, 'output/navigation.png')
    print("✅ Симуляция завершена. Данные в output/")

if __name__ == '__main__':
    main()
