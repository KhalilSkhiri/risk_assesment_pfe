# 📊 Statistical Analysis Module

Analyse probabiliste et régression linéaire pour les prédictions d'émissions de carbone.

## 📁 Structure

```
statistical_analysis/
├── __init__.py                 # Module initialization
├── regression_model.py         # Linear regression for emissions prediction
├── probability_analysis.py     # Probabilistic risk assessment
└── README.md                   # This file
```

## 🎯 Fonctionnalités

### 1. **Régression Linéaire** (`regression_model.py`)

Modèle de régression linéaire pour prédire les émissions futures basé sur les données historiques.

#### Utilisation

```python
from statistical_analysis.regression_model import LinearRegression

# Données historiques
years = [2020, 2021, 2022, 2023]
emissions = [5000, 5500, 6100, 6800]  # tCO2e

# Fit le modèle
regressor = LinearRegression()
model = regressor.fit(years, emissions)

# Prédictions
print(model)  # Affiche l'équation du modèle
print(f"R² = {model.r_squared:.4f}")

# Prédire pour une année future
pred_2024 = regressor.predict(2024)
print(f"Émissions 2024: {pred_2024:.2f} tCO2e")

# Prédictions multiples
future = regressor.predict_future(3)  # 3 prochaines années
for year, pred in future:
    print(f"{year}: {pred:.2f} tCO2e")

# Statistiques
stats = regressor.get_statistics()
print(f"Tendance: {stats['trend_direction']}")
```

**Paramètres du modèle:**
- **Slope (m)**: Pente de la régression (variation annuelle en tCO2e/an)
- **Intercept (b)**: Ordonnée à l'origine
- **R-squared**: Coefficient de détermination (0-1, plus proche de 1 = meilleur ajustement)
- **Std Error**: Erreur standard du modèle

---

### 2. **Analyse Probabiliste** (`probability_analysis.py`)

Évaluation du risque climatique et intervalles de confiance pour les prédictions.

#### Utilisation

```python
from statistical_analysis.probability_analysis import ProbabilityAnalyzer, RiskLevel

# Données historiques
historical_emissions = [4800, 5200, 5100, 5400, 5800, 6200]

# Analyse probabiliste
analyzer = ProbabilityAnalyzer(historical_emissions)

# Statistiques descriptives
stats = analyzer.get_statistics()
print(f"Moyenne: {stats['mean']:.2f} tCO2e")
print(f"Écart-type: {stats['std_dev']:.2f}")
print(f"Coefficient de variation: {stats['coefficient_of_variation']:.2f}")

# Percentiles
p25 = analyzer.percentile(25)
p75 = analyzer.percentile(75)
print(f"P25: {p25:.2f}, P75: {p75:.2f}")

# Intervalle de confiance (95%)
ci = analyzer.confidence_interval(point_estimate=6500, confidence_level=0.95)
print(f"IC 95%: [{ci.lower_bound:.2f}, {ci.upper_bound:.2f}]")

# Catégorisation du risque
risk = analyzer.categorize_risk(6500)
print(f"Niveau de risque: {risk.value}")  # LOW, MEDIUM, HIGH, CRITICAL

# Probabilités
prob_above_7000 = analyzer.probability_above_threshold(7000)
print(f"P(émissions > 7000) = {prob_above_7000:.2%}")

prob_5000_6000 = analyzer.probability_in_range(5000, 6000)
print(f"P(5000 < émissions < 6000) = {prob_5000_6000:.2%}")
```

**Niveaux de risque:**
- **LOW**: < 25e percentile (faible historiquement)
- **MEDIUM**: 25e - 75e percentile (normal)
- **HIGH**: > 75e percentile (élevé)
- **CRITICAL**: > 90e percentile (critique)

---

## 📈 Cas d'Usage

### Cas 1: Prédiction des émissions 2024-2026

```python
from statistical_analysis.regression_model import LinearRegression

# Historique 3 ans
years = [2021, 2022, 2023]
emissions = [4500, 5200, 5900]

regressor = LinearRegression()
regressor.fit(years, emissions)

predictions = regressor.predict_future(3)
for year, pred in predictions:
    print(f"{year}: {pred:.2f} tCO2e")
```

### Cas 2: Évaluation du risque d'une entreprise

```python
from statistical_analysis.probability_analysis import ProbabilityAnalyzer

# Émissions annuelles observées
emissions_history = [3000, 3200, 3100, 3400, 3600, 3300]

analyzer = ProbabilityAnalyzer(emissions_history)

# Émission prédite pour l'année prochaine
predicted = 3800

# Évaluer le risque
risk_level = analyzer.categorize_risk(predicted)
ci = analyzer.confidence_interval(predicted)

print(f"Prédiction: {predicted} tCO2e")
print(f"Risque: {risk_level.value}")
print(f"IC 95%: [{ci.lower_bound:.2f}, {ci.upper_bound:.2f}]")

# Probabilité de dépassement d'un seuil
prob = analyzer.probability_above_threshold(4000)
print(f"Probabilité dépassement 4000: {prob:.2%}")
```

---

## 🔧 Dépendances

Aucune dépendance externe requise. Utilise uniquement la stdlib Python:
- `math`
- `dataclasses`
- `typing`
- `enum`

---

## 📝 Notes Mathématiques

### Régression Linéaire (Méthode OLS)
- Modèle: $y = mx + b$
- Coefficient de détermination: $R^2 = 1 - \frac{SS_{res}}{SS_{tot}}$

### Analyse Probabiliste
- Distribution normale approximée pour les intervalles de confiance
- Z-scores: 1.645 (90%), 1.96 (95%), 2.576 (99%)
- Coefficient de variation: $CV = \frac{\sigma}{\mu}$

---

## ✅ Tests

```bash
cd pfe_project
python -m pytest tests/
```

---

## 📚 Références

- GHG Protocol Corporate Standard
- IPCC Guidelines for National Greenhouse Gas Inventories
- ISO 14064-2: Quantification and reporting of greenhouse gas emissions
