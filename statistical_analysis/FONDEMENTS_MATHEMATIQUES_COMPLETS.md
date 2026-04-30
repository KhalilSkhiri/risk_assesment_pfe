# 📊 Analyse Statistique et Mathématique pour la Prédiction d'Émissions Carbone

**Document pour l'encadrant**  
Version: 1.0  
Date: 27 avril 2026  
Projet: Calculateur d'Empreinte Carbone - Analyse ESG

---

## 📑 Table des matières

1. [Objectifs](#objectifs)
2. [Fondements Théoriques](#fondements-théoriques)
3. [Modèle 1: Régression Linéaire](#modèle-1-régression-linéaire)
4. [Modèle 2: Analyse Probabiliste](#modèle-2-analyse-probabiliste)
5. [Applications Pratiques](#applications-pratiques)
6. [Validation Statistique](#validation-statistique)
7. [Implémentation](#implémentation)

---

## 🎯 Objectifs

Ce module statistique vise à :

1. **Prédire** les émissions futures basées sur les données historiques
2. **Quantifier** l'incertitude des prédictions via des intervalles de confiance
3. **Évaluer** le risque climatique d'une entreprise
4. **Supporter** la prise de décision d'investissement bancaire

---

## 🧮 Fondements Théoriques

### A. Hypothèses de base

Le modèle repose sur les hypothèses suivantes :

#### 1. **Stationnarité faible**
Les données d'émissions $\{E_t\}_{t=1}^{n}$ satisfont :
- $E[\text{Émissions}_t] = \mu < \infty$ (espérance finie)
- $\text{Var}(\text{Émissions}_t) = \sigma^2 < \infty$ (variance finie et constante)
- $\text{Cov}(E_t, E_s) = 0$ pour $|t - s| > $ lag critique

#### 2. **Normalité asymptotique**
Par le **Théorème Central Limite**, pour $n$ suffisamment grand :
$$\frac{\bar{E} - \mu}{\sigma/\sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$$

où $\bar{E} = \frac{1}{n}\sum_{i=1}^n E_i$

#### 3. **Linéarité des tendances**
La tendance long-terme des émissions suit une relation linéaire :
$$E_t = \alpha + \beta \cdot t + \varepsilon_t$$

où $\varepsilon_t \sim \mathcal{N}(0, \sigma^2)$ (bruit blanc)

### B. Notation mathématique

| Symbole | Signification |
|---------|--------------|
| $n$ | Nombre d'observations historiques |
| $E_i$ | Émission à l'année $i$ (en tCO₂e) |
| $t_i$ | Année ou période $i$ |
| $\mu$ | Moyenne théorique |
| $\sigma^2$ | Variance théorique |
| $\hat{\mu}$, $\hat{\sigma}$ | Estimateurs empiriques |
| $\mathcal{N}(\mu, \sigma^2)$ | Distribution normale |

---

## 📈 Modèle 1: Régression Linéaire

### A. Formulation du problème

On observe $n$ paires $(t_i, E_i)$ où:
- $t_i \in \mathbb{R}$ : temps (année)
- $E_i \in \mathbb{R}^+$ : émissions observées

**Objectif:** Estimer les paramètres $(m, b)$ du modèle linéaire

$$\boxed{E = m \cdot t + b + \varepsilon}$$

où $\varepsilon \sim \mathcal{N}(0, \sigma^2)$ est l'erreur résiduelle.

### B. Méthode OLS (Ordinary Least Squares)

**Fonction de coût** (somme des carrés des résidus) :

$$\min_{m,b} L(m,b) = \sum_{i=1}^{n} (E_i - (m \cdot t_i + b))^2$$

#### B.1 Solution analytique

Les estimateurs OLS sont obtenus en posant $\frac{\partial L}{\partial m} = 0$ et $\frac{\partial L}{\partial b} = 0$ :

$$\frac{\partial L}{\partial m} = -2 \sum_{i=1}^{n} t_i(E_i - m \cdot t_i - b) = 0$$

$$\frac{\partial L}{\partial b} = -2 \sum_{i=1}^{n} (E_i - m \cdot t_i - b) = 0$$

**Résolution du système normal :**

$$\boxed{\hat{m} = \frac{\sum_{i=1}^{n} (t_i - \bar{t})(E_i - \bar{E})}{\sum_{i=1}^{n} (t_i - \bar{t})^2} = \frac{\text{Cov}(t, E)}{\text{Var}(t)}}$$

$$\boxed{\hat{b} = \bar{E} - \hat{m} \cdot \bar{t}}$$

où $\bar{t} = \frac{1}{n}\sum t_i$ et $\bar{E} = \frac{1}{n}\sum E_i$

#### B.2 Propriétés des estimateurs OLS

Sous les hypothèses de base, les estimateurs OLS satisfont :

1. **Non-biais** : $E[\hat{m}] = m$ et $E[\hat{b}] = b$

2. **Consistance** : $\hat{m} \xrightarrow{p} m$ et $\hat{b} \xrightarrow{p} b$ quand $n \to \infty$

3. **Efficacité** : Variance minimale parmi les estimateurs linéaires sans biais (BLUE)

4. **Normalité asymptotique** : 
   $$\sqrt{n}(\hat{m} - m) \xrightarrow{d} \mathcal{N}(0, \sigma_m^2)$$
   
   où $\sigma_m^2 = \frac{\sigma^2}{\sum(t_i - \bar{t})^2}$

### C. Mesure de qualité d'ajustement

#### C.1 Coefficient de détermination $R^2$

$$R^2 = \frac{\text{SS}_{\text{exp}}}{\text{SS}_{\text{tot}}} = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$$

où:
- $\text{SS}_{\text{tot}} = \sum_{i=1}^{n} (E_i - \bar{E})^2$ : somme totale des carrés
- $\text{SS}_{\text{res}} = \sum_{i=1}^{n} (E_i - \hat{E}_i)^2$ : somme des carrés des résidus
- $\text{SS}_{\text{exp}} = \sum_{i=1}^{n} (\hat{E}_i - \bar{E})^2$ : somme des carrés expliquée

**Interprétation** : $R^2$ représente la fraction de variance expliquée par le modèle.
- $R^2 = 1$ : ajustement parfait
- $R^2 = 0.9$ : très bon ajustement
- $R^2 = 0.7$ : ajustement acceptable
- $R^2 < 0.5$ : ajustement faible

#### C.2 Adjusted R²

Pour tenir compte du nombre de paramètres :

$$R^2_{\text{adj}} = 1 - \frac{(1 - R^2)(n - 1)}{n - p - 1}$$

où $p = 1$ est le nombre de variables explicatives (le temps).

#### C.3 Erreur standard de l'estimation

$$\hat{\sigma}^2 = \frac{\text{SS}_{\text{res}}}{n - 2} = \frac{1}{n-2}\sum_{i=1}^{n} (E_i - \hat{E}_i)^2$$

$$\hat{\sigma} = \sqrt{\hat{\sigma}^2} \quad \text{(erreur standard)}$$

#### C.4 Erreur standard de la pente

$$\text{SE}(\hat{m}) = \frac{\hat{\sigma}}{\sqrt{\sum_{i=1}^{n}(t_i - \bar{t})^2}}$$

### D. Prédiction et intervalle de confiance

#### D.1 Prédiction ponctuelle

Pour une année future $t^*$ :

$$\boxed{\hat{E}(t^*) = \hat{m} \cdot t^* + \hat{b}}$$

#### D.2 Intervalle de confiance pour la prédiction

La variance de la prédiction est :

$$\text{Var}(\hat{E}(t^*)) = \sigma^2 \left(1 + \frac{1}{n} + \frac{(t^* - \bar{t})^2}{\sum_{i=1}^{n}(t_i - \bar{t})^2}\right)$$

L'intervalle de confiance à niveau $1 - \alpha$ est :

$$\boxed{\hat{E}(t^*) \pm t_{n-2, \alpha/2} \cdot \sqrt{\text{Var}(\hat{E}(t^*))}}$$

où $t_{n-2, \alpha/2}$ est le quantile $\alpha/2$ de la distribution de Student avec $n-2$ degrés de liberté.

#### D.3 Cas particulier: $n$ grand

Quand $n \to \infty$, on utilise l'approximation normale :

$$t_{n-2, \alpha/2} \approx z_{\alpha/2}$$

où:
- $z_{0.05} = 1.645$ pour IC 90%
- $z_{0.025} = 1.96$ pour IC 95%
- $z_{0.005} = 2.576$ pour IC 99%

#### D.4 Analyse des résidus

Les résidus $e_i = E_i - \hat{E}_i$ doivent satisfaire :

1. **Normalité** : $e_i \sim \mathcal{N}(0, \sigma^2)$ (test de Shapiro-Wilk)
2. **Homoscédasticité** : $\text{Var}(e_i)$ constant (test de Breusch-Pagan)
3. **Indépendance** : $\text{Cov}(e_i, e_j) = 0$ pour $i \neq j$ (test de Durbin-Watson)
4. **Pas d'outliers** : Résidus normalisés $|e_i/\hat{\sigma}| < 3$

---

## 🎲 Modèle 2: Analyse Probabiliste

### A. Statistiques descriptives

#### A.1 Moyenne empirique

$$\hat{\mu} = \bar{E} = \frac{1}{n}\sum_{i=1}^{n} E_i$$

C'est un estimateur sans biais et convergent de $\mu$.

#### A.2 Variance empirique

$$\hat{\sigma}^2 = \frac{1}{n-1}\sum_{i=1}^{n}(E_i - \bar{E})^2$$

(On divise par $n-1$ pour obtenir un estimateur sans biais - correction de Bessel)

#### A.3 Coefficient de variation

$$CV = \frac{\hat{\sigma}}{\hat{\mu}}$$

Mesure la volatilité relative. Utile pour comparer la variabilité entre entreprises.

### B. Distribution des émissions

#### B.1 Hypothèse de normalité

Sous l'hypothèse que $E \sim \mathcal{N}(\mu, \sigma^2)$, la fonction de densité est :

$$f(E) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(E-\mu)^2}{2\sigma^2}\right)$$

#### B.2 Validation de la normalité

**Test de Shapiro-Wilk** (pour $n < 50$) :

$H_0$: Les données suivent une distribution normale  
$H_1$: Les données ne suivent pas une distribution normale

**Test de Kolmogorov-Smirnov** (pour tout $n$) :

$$D_n = \max_{E} |F_n(E) - F(E)|$$

où $F_n$ est la CDF empirique et $F$ est la CDF normale.

#### B.3 Transformation en cas de non-normalité

Si la normalité est rejetée, on peut utiliser une **transformation Box-Cox** :

$$E^{(\lambda)} = \begin{cases}
\frac{E^\lambda - 1}{\lambda} & \text{si } \lambda \neq 0 \\
\ln(E) & \text{si } \lambda = 0
\end{cases}$$

### C. Percentiles

#### C.1 Définition

Le percentile $p$ (pour $0 < p < 100$) est la valeur $q_p$ telle que :

$$P(E \leq q_p) = \frac{p}{100}$$

#### C.2 Calcul empirique

Pour les données triées $E_{(1)} \leq E_{(2)} \leq \cdots \leq E_{(n)}$ :

**Méthode 1 (Linéaire)** :
$$q_p = E_{(j)} + (E_{(j+1)} - E_{(j)}) \cdot f$$

où $j = \lfloor \frac{p \cdot n}{100} \rfloor$ et $f = \text{frac}\left(\frac{p \cdot n}{100}\right)$

**Méthode 2 (Nearest rank)** :
$$q_p = E_{(\lceil p \cdot n / 100 \rceil)}$$

#### C.3 Quartiles et IQR

- $Q_1 = q_{25}$ : premier quartile
- $Q_2 = q_{50}$ : médiane
- $Q_3 = q_{75}$ : troisième quartile
- $\text{IQR} = Q_3 - Q_1$ : écart interquartile

### D. Intervalles de confiance

#### D.1 IC pour la moyenne

Sous normalité avec $\sigma$ inconnu :

$$\boxed{\bar{E} \pm t_{n-1, \alpha/2} \cdot \frac{\hat{\sigma}}{\sqrt{n}}}$$

où le demi-largeur est appelée **marge d'erreur** :

$$ME = t_{n-1, \alpha/2} \cdot \frac{\hat{\sigma}}{\sqrt{n}}$$

#### D.2 IC pour une observation future

Pour prédire la valeur d'une **seule observation future** (pas la moyenne) :

$$\boxed{\bar{E} \pm t_{n-1, \alpha/2} \cdot \hat{\sigma} \cdot \sqrt{1 + \frac{1}{n}}}$$

Notez le terme $\sqrt{1 + \frac{1}{n}}$ qui rend cet intervalle plus large.

#### D.3 Niveau de confiance usuel

| Niveau | $\alpha$ | $z_{\alpha/2}$ | $t_{n-1, \alpha/2}$ |
|--------|----------|---|---|
| 90% | 0.10 | 1.645 | ~1.64 ($n$ grand) |
| 95% | 0.05 | 1.96 | ~1.96 ($n$ grand) |
| 99% | 0.01 | 2.576 | ~2.576 ($n$ grand) |

### E. Catégorisation du risque

#### E.1 Système de classification

Basé sur la position dans la distribution empirique :

$$\text{RiskLevel}(E) = \begin{cases}
\text{LOW} & \text{si } E \leq Q_1 \, (p \leq 25\%) \\
\text{MEDIUM} & \text{si } Q_1 < E \leq Q_3 \, (25\% < p \leq 75\%) \\
\text{HIGH} & \text{si } Q_3 < E \leq p_{90} \, (75\% < p \leq 90\%) \\
\text{CRITICAL} & \text{si } E > p_{90} \, (p > 90\%)
\end{cases}$$

#### E.2 Justification statistique

- **LOW** : Performance parmi les 25% meilleures
- **MEDIUM** : Performance moyenne (dans les 50% centraux)
- **HIGH** : Performance dégradée (top 25% pire)
- **CRITICAL** : Performance très dégradée (top 10% pire)

### F. Probabilités et fonction de survie

#### F.1 Probabilité de dépassement

Sous normalité $E \sim \mathcal{N}(\mu, \sigma^2)$ :

$$P(E > e_0) = 1 - \Phi\left(\frac{e_0 - \mu}{\sigma}\right)$$

où $\Phi$ est la CDF de la distribution normale standard.

**Transformation en z-score** :

$$z = \frac{e_0 - \mu}{\sigma}$$

$$P(E > e_0) = 1 - \Phi(z) = Q(z)$$

où $Q(z)$ est la **fonction de survie** (tail probability).

#### F.2 Probabilité dans un intervalle

$$P(e_1 \leq E \leq e_2) = \Phi\left(\frac{e_2 - \mu}{\sigma}\right) - \Phi\left(\frac{e_1 - \mu}{\sigma}\right)$$

#### F.3 Approximation de la CDF normale

**Approximation analytique rapide** (erreur < 0.0002) :

$$\Phi(z) \approx \begin{cases}
\frac{1}{2} + \frac{z}{\sqrt{2\pi}} e^{-z^2/2} \left(a_1 t + a_2 t^2 + a_3 t^3\right) & z \geq 0 \\
1 - \Phi(-z) & z < 0
\end{cases}$$

où $t = \frac{1}{1 + pz}$ et $p, a_1, a_2, a_3$ sont des constantes de Abramowitz-Stegun.

**Cas simple utilisé ici** :

$$\Phi(z) = \frac{1}{2}\left(1 + \text{erf}\left(\frac{z}{\sqrt{2}}\right)\right)$$

où $\text{erf}$ est la fonction d'erreur (fournie par math.erf en Python).

---

## 📊 Applications Pratiques

### Application 1: Prédiction d'émissions futures

**Scénario**: Une entreprise a des émissions de:
- 2020: 4500 tCO₂e
- 2021: 5100 tCO₂e
- 2022: 5800 tCO₂e
- 2023: 6400 tCO₂e

**Calculs**:

$$\bar{t} = \frac{2020 + 2021 + 2022 + 2023}{4} = 2021.5$$
$$\bar{E} = \frac{4500 + 5100 + 5800 + 6400}{4} = 5450$$

$$\sum(t_i - \bar{t})^2 = (-1.5)^2 + (-0.5)^2 + (0.5)^2 + (1.5)^2 = 5$$

$$\sum(t_i - \bar{t})(E_i - \bar{E}) = (-1.5)(-950) + (-0.5)(-350) + (0.5)(350) + (1.5)(950) = 3150$$

$$\hat{m} = \frac{3150}{5} = 630 \text{ tCO}_2\text{e/an}$$

$$\hat{b} = 5450 - 630 \times 2021.5 = -1,274,545$$

**Prédiction pour 2024** :

$$\hat{E}(2024) = 630 \times 2024 - 1,274,545 = 7030 \text{ tCO}_2\text{e}$$

Soit une **croissance annuelle d'environ 630 tCO₂e/an** (environ 11.5% par an).

### Application 2: Évaluation du risque climatique

**Données** : Historique de 6 ans d'une entreprise
$$E = [3200, 3400, 3500, 3800, 4100, 4400] \text{ tCO}_2\text{e}$$

**Statistiques descriptives** :

$$\hat{\mu} = 3733 \text{ tCO}_2\text{e}$$
$$\hat{\sigma} = 437 \text{ tCO}_2\text{e}$$
$$CV = 0.117 \text{ (11.7% de volatilité)}$$

**Percentiles** :

$$Q_1 = 3350 \text{ tCO}_2\text{e}$$
$$Q_2 = 3650 \text{ tCO}_2\text{e} \text{ (médiane)}$$
$$Q_3 = 3950 \text{ tCO}_2\text{e}$$

**Catégorisation d'une prédiction de 4200 tCO₂e** :

Comme $4200 > Q_3 = 3950$, le risque est **HIGH**.

**Probabilité de dépassement** :

$$z = \frac{4500 - 3733}{437} = 1.75$$
$$P(E > 4500) = 1 - \Phi(1.75) \approx 0.04 \text{ (4%)}$$

Il y a environ **4% de chance que les émissions dépassent 4500 tCO₂e**.

### Application 3: Rapport d'investissement

**Combinaison régression + probabilité** :

1. **Tendance** : Régression OLS avec $\hat{m} = 630$ tCO₂e/an → **CROISSANCE**
2. **Volatilité** : CV = 11.7% → **STABLE**
3. **Prédiction 2024** : 7030 tCO₂e
4. **IC 95%** : [6400, 7660] tCO₂e
5. **Risque** : HIGH (car au-delà de Q₃)

**Recommandation** : ⚠️ **CONDITIONAL**
- Points négatifs: Croissance rapide des émissions
- Points positifs: Volatilité acceptable

---

## ✅ Validation Statistique

### A. Tests de validation du modèle OLS

#### A.1 Test de normalité des résidus (Shapiro-Wilk)

$H_0$: Les résidus suivent une distribution normale  
$H_1$: Les résidus ne suivent pas une distribution normale

**Décision** : Rejeter $H_0$ si p-value < 0.05

#### A.2 Test d'hétéroscédasticité (Breusch-Pagan)

$H_0$: $\text{Var}(\varepsilon_i) = \sigma^2$ (homoscédasticité)  
$H_1$: $\text{Var}(\varepsilon_i) \neq \sigma^2$ (hétéroscédasticité)

**Statistique de test** :

$$BP = \frac{1}{2} \sum_{i=1}^{n} (e_i/\hat{\sigma})^2$$

#### A.3 Test d'auto-corrélation (Durbin-Watson)

$$DW = \frac{\sum_{i=2}^{n}(e_i - e_{i-1})^2}{\sum_{i=1}^{n} e_i^2}$$

**Interprétation** :
- $DW \approx 2$ : Pas d'auto-corrélation ✓
- $DW < 2$ : Auto-corrélation positive
- $DW > 2$ : Auto-corrélation négative

**Valeurs critiques** (pour $n = 20, p = 1$) :
- $d_L = 1.20$, $d_U = 1.41$
- Pas d'auto-corrélation si $1.41 < DW < 2.59$

#### A.4 Test de significativité de la pente

$H_0$: $\beta = 0$ (pas de tendance)  
$H_1$: $\beta \neq 0$ (tendance présente)

**Statistique de test** :

$$t = \frac{\hat{m} - 0}{\text{SE}(\hat{m})} = \frac{\hat{m}\sqrt{\sum(t_i - \bar{t})^2}}{\hat{\sigma}}$$

**Décision** : Rejeter $H_0$ si $|t| > t_{n-2, \alpha/2}$

### B. Métriques de diagnostic

| Métrique | Bon | Acceptable | Mauvais |
|----------|-----|-----------|---------|
| $R^2$ | > 0.9 | 0.7 - 0.9 | < 0.7 |
| DW | 1.5 - 2.5 | 1.2 - 2.8 | < 1.2 ou > 2.8 |
| RMSE | < 10% de $\bar{E}$ | 10-20% | > 20% |
| p-value (pente) | < 0.05 | 0.05 - 0.10 | > 0.10 |

---

## 💻 Implémentation

### A. Architecture du code

```
statistical_analysis/
├── regression_model.py      # OLS regression
├── probability_analysis.py  # Probabilistic analysis
├── utils.py                 # Helper functions
├── examples.py              # Use cases
└── integration.py           # Integration guide
```

### B. Dépendances minimales

```python
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
```

**Aucune dépendance externe** : Utilise uniquement la stdlib Python.

### C. Classe RegressionModel

```python
@dataclass
class RegressionModel:
    slope: float           # m
    intercept: float       # b
    r_squared: float       # R²
    std_error: float       # σ
    
    def predict(self, x: float) -> float:
        return self.slope * x + self.intercept
```

### D. Classe ProbabilityAnalyzer

```python
class ProbabilityAnalyzer:
    def __init__(self, data: List[float]):
        self.data = data
        self.mean = self._calculate_mean()
        self.std_dev = self._calculate_std_dev()
    
    def confidence_interval(self, estimate: float, 
                          confidence_level: float = 0.95) -> ConfidenceInterval:
        z_score = self._get_z_score(confidence_level)
        margin = z_score * self.std_dev
        return ConfidenceInterval(estimate - margin, estimate, 
                                estimate + margin, confidence_level)
```

### E. Usage example

```python
from statistical_analysis.regression_model import LinearRegression
from statistical_analysis.probability_analysis import ProbabilityAnalyzer

# Données
years = [2020, 2021, 2022, 2023]
emissions = [5000, 5500, 6100, 6800]

# Régression
reg = LinearRegression()
model = reg.fit(years, emissions)
print(f"Prédiction 2024: {reg.predict(2024):.0f} tCO2e")

# Probabilité
analyzer = ProbabilityAnalyzer(emissions)
ci = analyzer.confidence_interval(6800, confidence_level=0.95)
print(f"IC 95%: [{ci.lower_bound:.0f}, {ci.upper_bound:.0f}]")
```

---

## 📚 Références Mathématiques

### Livres

1. **Greene, W. H. (2012).** *Econometric Analysis* (7th ed.). Prentice Hall.
   - Chapitre 2: Least Squares Regression

2. **Wackerly, D. D., Mendenhall III, W., & Scheaffer, R. L. (2014).** *Mathematical Statistics with Applications* (7th ed.).
   - Chapitre 8: Inference Based on a Single Sample

3. **Chatterjee, S., & Hadi, A. S. (2015).** *Regression Analysis by Example* (5th ed.). Wiley.

### Articles et normes

4. **IPCC (2006).** *2006 IPCC Guidelines for National Greenhouse Gas Inventories.*
   - Methods for uncertainty estimation

5. **Hastie, T., Tibshirani, R., & Friedman, J. (2009).** *The Elements of Statistical Learning* (2nd ed.). Springer.
   - Chapitre 3: Linear Regression Models

### Standards statistiques

6. **ISO 13528:2015** - Guidance for the use of proficiency testing in method validation
7. **JCGM 100:2008** - Evaluation of measurement data — Guide to the expression of uncertainty in measurement

---

## 🔍 Annexe: Formules clés résumées

### Régression Linéaire

$$\boxed{\hat{m} = \frac{\sum(t_i - \bar{t})(E_i - \bar{E})}{\sum(t_i - \bar{t})^2}} \quad \boxed{\hat{b} = \bar{E} - \hat{m}\bar{t}}$$

$$\boxed{R^2 = 1 - \frac{\sum(E_i - \hat{E}_i)^2}{\sum(E_i - \bar{E})^2}} \quad \boxed{\text{SE}(\hat{m}) = \frac{\hat{\sigma}}{\sqrt{\sum(t_i - \bar{t})^2}}}$$

### Analyse Probabiliste

$$\boxed{\hat{\mu} = \bar{E}} \quad \boxed{\hat{\sigma} = \sqrt{\frac{1}{n-1}\sum(E_i - \bar{E})^2}} \quad \boxed{CV = \frac{\hat{\sigma}}{\hat{\mu}}}$$

$$\boxed{\text{IC}_{1-\alpha} = \bar{E} \pm z_{\alpha/2} \cdot \frac{\hat{\sigma}}{\sqrt{n}}} \quad \boxed{P(E > e_0) = 1 - \Phi\left(\frac{e_0 - \mu}{\sigma}\right)}$$

---

**Document préparé pour l'encadrant académique**  
*Version 1.0 - 27 avril 2026*
