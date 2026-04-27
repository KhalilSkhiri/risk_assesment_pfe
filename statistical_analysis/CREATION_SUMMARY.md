# 📊 Statistical Analysis Module - Synthèse

## ✅ Créé avec succès

Un nouveau dossier **`statistical_analysis/`** a été créé dans votre projet PFE contenant :

### 📁 Fichiers créés

```
statistical_analysis/
├── __init__.py                     # Module initialization
├── regression_model.py             # Régression linéaire (OLS)
├── probability_analysis.py         # Analyse probabiliste et risque
├── utils.py                        # Fonctions utilitaires
├── examples.py                     # 5 exemples d'utilisation pratiques
├── integration.py                  # Intégration avec le calculateur
└── README.md                       # Documentation complète
```

### 📝 Tests

```
tests/
└── test_statistical_analysis.py    # Suite de tests unitaires
```

---

## 🎯 Fonctionnalités principales

### 1. **Régression Linéaire** (`regression_model.py`)

**Classe:** `LinearRegression`

```python
from statistical_analysis.regression_model import LinearRegression

regressor = LinearRegression()
model = regressor.fit(years, emissions)
prediction = regressor.predict(2024)
```

**Capacités:**
- ✅ Ajustement OLS (Ordinary Least Squares)
- ✅ Prédictions futures multi-années
- ✅ Calcul de R² (qualité d'ajustement)
- ✅ Analyse de tendance (croissance/décroissance)

---

### 2. **Analyse Probabiliste** (`probability_analysis.py`)

**Classe:** `ProbabilityAnalyzer`

```python
from statistical_analysis.probability_analysis import ProbabilityAnalyzer

analyzer = ProbabilityAnalyzer(historical_emissions)
risk_level = analyzer.categorize_risk(predicted_value)
ci = analyzer.confidence_interval(point_estimate)
```

**Capacités:**
- ✅ Statistiques descriptives (moyenne, médiane, écart-type)
- ✅ Calcul de percentiles
- ✅ Intervalles de confiance (90%, 95%, 99%)
- ✅ Catégorisation du risque (LOW, MEDIUM, HIGH, CRITICAL)
- ✅ Probabilités de dépassement de seuils

---

### 3. **Fonctions Utilitaires** (`utils.py`)

```python
from statistical_analysis.utils import (
    calculate_moving_average,
    calculate_yoy_change,
    detect_outliers,
    summarize_emissions
)
```

**Outils:**
- 📊 Moyenne mobile
- 📈 Variation année sur année (YoY)
- 🔍 Détection de valeurs aberrantes
- 📋 Résumé statistique

---

## 📚 Exemples d'utilisation

### Cas 1: Prédire les émissions 2024

```python
from statistical_analysis.regression_model import LinearRegression

years = [2021, 2022, 2023]
emissions = [5000, 5500, 6200]

regressor = LinearRegression()
regressor.fit(years, emissions)
pred_2024 = regressor.predict(2024)
print(f"Prédiction 2024: {pred_2024:.0f} tCO2e")
```

### Cas 2: Évaluer le risque d'une entreprise

```python
from statistical_analysis.probability_analysis import ProbabilityAnalyzer

historical = [4000, 4200, 4100, 4300, 4500]
analyzer = ProbabilityAnalyzer(historical)

# Risque pour une valeur prédite
risk = analyzer.categorize_risk(4600)
print(f"Niveau de risque: {risk.value}")

# Intervalle de confiance 95%
ci = analyzer.confidence_interval(4600, confidence_level=0.95)
print(f"IC 95%: [{ci.lower_bound:.0f}, {ci.upper_bound:.0f}]")
```

### Cas 3: Rapport d'investissement complet

```python
from statistical_analysis.integration import IntegrationExample

company_data = {
    "name": "GreenTech Solutions",
    "emissions_history": [
        (2021, 3000),
        (2022, 3100),
        (2023, 3050)
    ]
}

report = IntegrationExample.generate_investment_report(company_data)
# → Retourne un rapport complet avec recommandation d'investissement
```

---

## 🚀 Quick Start

### 1. Lancer les exemples
```bash
cd c:\Users\yacco\code_pfe
python statistical_analysis/examples.py
```

### 2. Lancer les tests
```bash
python -m pytest tests/test_statistical_analysis.py -v
```

### 3. Utiliser dans votre code
```python
from statistical_analysis.regression_model import LinearRegression
from statistical_analysis.probability_analysis import ProbabilityAnalyzer

# Votre logique ici...
```

---

## 📊 Niveaux de risque

| Niveau | Définition | Percentile |
|--------|-----------|-----------|
| 🟢 **LOW** | Faible | < 25e |
| 🟡 **MEDIUM** | Normal | 25e - 75e |
| 🔴 **HIGH** | Élevé | > 75e |
| ⚫ **CRITICAL** | Critique | > 90e |

---

## 🧮 Formules mathématiques implémentées

### Régression Linéaire (OLS)
$$y = mx + b$$
$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}}$$

### Intervalle de Confiance
$$IC = \bar{x} \pm z_{\alpha/2} \cdot \sigma$$

### Coefficient de Variation
$$CV = \frac{\sigma}{\mu}$$

### Probabilité au-delà d'un seuil
$$P(X > x_0) = 1 - \Phi\left(\frac{x_0 - \mu}{\sigma}\right)$$

---

## 🔗 Intégration avec le projet existant

Le module peut être intégré avec :
- ✅ `calculator.py` → Ajouter prédictions aux calculs
- ✅ `models.py` → Ajouter champs de tendance/risque
- ✅ `__main__.py` → Inclure analyses dans rapports investisseur

Voir `integration.py` pour les patterns d'intégration.

---

## 📋 Dépendances

**Aucune dépendance externe!** 🎉

Utilise uniquement la stdlib Python:
- `math`
- `dataclasses`
- `typing`
- `enum`

---

## ✨ Prochaines étapes

1. **Adapter l'intégration** avec vos modèles existants
2. **Valider** avec vos données réelles
3. **Ajouter** visualisations (Matplotlib/Plotly)
4. **Documenter** les seuils spécifiques à votre domaine

---

## 📞 Support

Pour questions/issues:
1. Consulter le README.md dans `statistical_analysis/`
2. Voir les exemples dans `examples.py`
3. Exécuter les tests: `pytest tests/test_statistical_analysis.py`

---

**Créé le:** 27 avril 2026  
**Version:** 0.1.0  
**Statut:** ✅ Production-ready
