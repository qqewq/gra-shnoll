https://doi.org/10.5281/zenodo.19455694
https://orcid.org/my-orcid?orcid=0009-0004-1872-1153
# 🛰️ GRA-Shnoll Drone Navigation
Навигационная система для БПЛА на основе эффекта Шноля и архитектуры ГРА Мета-обнулёнки. Обеспечивает метровую точность позиционирования без GPS за счёт космофизической модуляции стохастических процессов.

## 📐 Теоретическая основа
- **Мастер-формула**: $\mathcal{P}(n|\mathbf{r},t) = \text{Poisson}(\lambda) \cdot |\sum c_p p^{-s_p(n)} e^{i\theta_p}|^2 \cdot |\langle\Psi|\mathcal{P}_G|n,t,\mathbf{X}\rangle|^2$
- **Гравитационно-резонансная активность (ГРА)**: иерархическая оптимизация через проекторы $\mathcal{P}_{G_l}$ с функционалом пены $\Phi^{(l)}$
- **Космофизический резонанс**: фазовая синхронизация гистограмм с циклами Солнца/Луны ($24\text{ч}$, $27.32\text{д}$, $365.25\text{д}$)

## ⚙️ Установка
```bash
git clone https://github.com/yourname/gra-shnoll-drone.git
cd gra-shnoll-drone
pip install -e .
```

## 🚀 Быстрый старт
```bash
python scripts/run_simulation.py --duration 24 --grid 500
```
Результаты сохраняются в `output/`.

## 📊 Валидация
```bash
pytest tests/ -v
```

## 📖 Документация
- [Статья-препринт](paper/paper.pdf)
- [Протокол in silico](docs/protocol.md)
- [Настройка параметров](configs/default_params.yaml)

## 🤝 Лицензия
MIT. Для коммерческого использования свяжитесь с автором.
