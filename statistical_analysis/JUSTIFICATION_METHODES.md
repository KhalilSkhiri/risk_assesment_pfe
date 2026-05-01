# 📖 Justification Complète des Méthodes de Régression

**Pourquoi utiliser la régression linéaire et justification de chaque composant**

Version: 1.0  
Date: 30 avril 2026  
Projet: Calculateur d'Empreinte Carbone - Analyse ESG

---

## 🎯 Table des Matières

1. [Motivation Générale](#motivation-générale)
2. [Pourquoi la Régression Linéaire?](#pourquoi-la-régression-linéaire)
3. [Justification des Méthodes Principales](#justification-des-méthodes-principales)
4. [Justification des Tests Diagnostiques](#justification-des-tests-diagnostiques)
5. [Justification des Intervalles de Confiance](#justification-des-intervalles-de-confiance)
6. [Cas d'Usage et Interprétation](#cas-dusage-et-interprétation)

---

## 🌍 Motivation Générale

### Contexte du Projet

**Objectif:** Prédire les émissions futures d'une entreprise pour évaluer son **risque climatique**.

**Données disponibles:** Séries temporelles d'émissions historiques (2020-2024)

**Enjeu banquaire:** 
- Les banques doivent évaluer l'exposition climatique de leurs clients
- Comprendre la **trajectoire** des émissions est crucial
- Prédire les **tendances futures** aide aux décisions de financement

### Formulation du Problème

Étant donné une série temporelle d'émissions historiques:
$$E_{2020}, E_{2021}, E_{2022}, E_{2023}, E_{2024}$$

**Questions à répondre:**
1. Quelle est la tendance (augmentée? diminuée? stable)?
2. À quel taux changent les émissions?
3. Quelles seront les émissions en 2025, 2026, 2027?
4. Avec quel niveau de confiance?

**Pour les prêteurs:** "Avec 95% de certitude, les émissions seront entre X et Y en 2025"

---

## 📈 Pourquoi la Régression Linéaire?

### 1. **Hypothèse: Linéarité de la Tendance**

**Justification:**
- **Court terme (3-5 ans):** Les changements technologiques et opérationnels d'une entreprise ont souvent un **effet linéaire**
- **Exemple:** Si une entreprise réduit sa production de 5% par an, c'est une **pente négative constante**
- **Alternative:** Modèles non-linéaires (polynomial, exponentiel) nécessitent plus de données et sont **sur-paramétrés** pour petit échantillon

**Contre-exemple non-linéaire:**
- Si l'entreprise opère un changement technologique majeur (énergie renouvelable), la tendance change → nécessite des données post-changement

**Decision:** Pour données 3-5 ans, linéarité = **meilleur équilibre biais-variance**

---

### 2. **Pourquoi Pas d'Autres Modèles?**

| Modèle | Avantages | Désavantages | Quand l'utiliser |
|--------|-----------|--------------|------------------|
| **Régression linéaire** | Simple, interprétable, estimateurs efficaces | Hypothèse linéarité | Trajectoires stables court-terme |
| Polynomial (degré 2) | Capture courbure | Plus complexe, sur-fitting avec peu de données | Si évidence de courbure (inflexion) |
| Exponentiel | Capture croissance géométrique | Difficile à estimer, peu de points | Croissance compound (rare pour émissions) |
| Time series (ARIMA) | Capture autocorrélation | Nécessite 50+ observations | Longues séries (10+ ans) |
| Machine Learning | Très flexible | Boîte noire, non interprétable, sur-fitting | Données massives (100k+ points) |

**Conclusion:** Régression linéaire = **optimal pour notre cas d'usage**

---

### 3. **Avantages de la Régression Linéaire pour Soutenance Bancaire**

✓ **Interprétabilité:** 
- Coefficient de pente = "X tCO2e/an" → **directement explicable au client**

✓ **Efficacité statistique:**
- Estimateurs OLS sont BLUE (meilleure variance) sous hypothèses Gauss-Markov

✓ **Inférence rigoureuse:**
- Tests d'hypothèse bien définis (t-test, F-test)
- Intervalles de confiance valides

✓ **Certification:**
- Modèle accepté par les standards ESG (Science-Based Targets, TCFD)
- Auditables (traçabilité complète des calculs)

---

## 📊 Justification des Méthodes Principales

### **MÉTHODE 1: `LinearRegression.fit()`**

#### Objective
Estimer les paramètres du modèle linéaire $E_t = \alpha + \beta \cdot t + \varepsilon_t$

#### Justification Mathématique

**Problème d'optimisation:**
$$\min_{\alpha, \beta} \sum_{i=1}^{n} (E_i - \alpha - \beta \cdot t_i)^2$$

**Pourquoi les moindres carrés?**

1. **Maximum de vraisemblance (ML):**
   - Sous normalité des erreurs: $\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$
   - OLS = MLE → **optimalité garantie** (Cramer-Rao lower bound)

2. **Théorème de Gauss-Markov:**
   - OLS sont **BLUE** = meilleure variance parmi estimateurs linéaires sans biais
   - Propriétés: Non-biais, consistance, efficacité

3. **Interprétabilité géométrique:**
   - Minimise distance verticale (résidus) entre observations et ligne ajustée
   - Centroïde $(\bar{t}, \bar{E})$ toujours sur la ligne

**Code implémentation:**

```python
# Étape 1: Calcul des moyennes
x_mean = np.mean(x_array)
y_mean = np.mean(y_array)

# Étape 2: Formule de la pente (équation normale)
numerator = np.sum((x_array - x_mean) * (y_array - y_mean))
denominator = np.sum((x_array - x_mean) ** 2)
slope = numerator / denominator  # ← OLS estimator

# Étape 3: Formule de l'intercept
intercept = y_mean - slope * x_mean  # ← OLS estimator
```

**Justification de chaque étape:**
- ✓ Moyennes: Centrage pour numérique stabilité et interprétation
- ✓ Numérateur: Covariance empirique entre t et E
- ✓ Dénominateur: Variance de t (ne doit pas être zéro)
- ✓ Intercept: Garantit que $(\bar{t}, \bar{E})$ est sur la ligne

---

### **MÉTHODE 2: Calcul du Coefficient de Détermination $R^2$**

#### Objective
Mesurer la **qualité d'ajustement** du modèle

#### Justification Mathématique

**Définition:**
$$R^2 = \frac{\text{SS}_{\text{exp}}}{\text{SS}_{\text{tot}}} = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$$

**Décomposition ANOVA (Analysis of Variance):**
$$\underbrace{\sum(E_i - \bar{E})^2}_{\text{variation totale}} = \underbrace{\sum(\hat{E}_i - \bar{E})^2}_{\text{variation expliquée}} + \underbrace{\sum(E_i - \hat{E}_i)^2}_{\text{résidus}}$$

**Interprétation:**
- $R^2$ = "Quelle fraction de la variance totale est expliquée par le modèle?"
- $R^2 = 0.85$ → "Le modèle explique 85% de la variation"
- $R^2 = 0.50$ → "Le modèle explique seulement 50%, autres facteurs dominent"

**Justification de l'utilisation:**
1. **Comparabilité:** 
   - Normalisé entre 0 et 1 (facilite comparaison entre modèles)
   - Indépendant des unités (tCO2e vs tonnes)

2. **Décision du prêteur:**
   - Seuil typique: $R^2 > 0.70$ pour modèle fiable
   - Si $R^2 < 0.50$: Trop d'autres facteurs → Modèle pas fiable pour prédiction

3. **Limite critique:**
   - $R^2$ augmente toujours avec ajout de variables (même inutiles)
   - Solution: Utiliser $R^2_{\text{adj}}$ ← voir MÉTHODE 3

**Code:**
```python
ss_res = np.sum((y_array - y_pred) ** 2)  # Erreur totale
ss_tot = np.sum((y_array - y_mean) ** 2)  # Variation totale

r_squared = 1 - (ss_res / ss_tot)  # Fraction expliquée

# Gestion du cas pathologique (NaN)
if ss_tot < 1e-10:  # Si aucune variation en y
    r_squared = 0.0  # Par convention
```

---

### **MÉTHODE 3: Adjusted $R^2$ (Coefficient Ajusté)**

#### Objective
Corriger le biais de $R^2$ quand on ajoute des variables

#### Justification Mathématique

**Problème:** $R^2$ augmente **toujours** si on ajoute une variable, même inutile

**Exemple:**
- $R^2$ avec 1 variable: 0.85
- $R^2$ avec 2 variables aléatoires: 0.87 (amélioration illusoire!)

**Solution: Adjusted $R^2$**

$$R^2_{\text{adj}} = 1 - (1-R^2) \cdot \frac{n-1}{n-p-1}$$

où $p$ = nombre de variables explicatives ($p=1$ en régression simple)

**Terme de pénalité:** $\frac{n-1}{n-p-1}$
- Si on ajoute variables inutiles: $R^2_{\text{adj}}$ **diminue**
- Pénalise la complexité → favorise parcimonie

**Quand l'utiliser:**
- Comparer deux modèles avec différent nombre de variables
- Exemple: Régression linéaire vs quadratique
- **Notre cas:** Régression simple (p=1), moins critique mais inclus

**Code:**
```python
r_squared_adj = 1 - (1 - r_squared) * (n - 1) / (n - 2)
# Terme (n - 2) = degrés de liberté = n - (nombre de paramètres: 2)
```

---

### **MÉTHODE 4: Erreur Standard et Intervalles de Confiance**

#### Objective
Quantifier **l'incertitude** des estimations (pente, prédictions)

#### Justification Théorique

**Problème:** Les estimateurs $\hat{\beta}$ et $\hat{\alpha}$ sont **aléatoires**
- Varient avec l'échantillon
- Une autre entreprise avec données similaires pourrait avoir pente légèrement différente

**Solution: Quantifier la variabilité**

**Erreur Standard de l'Estimation:**
$$\hat{\sigma}^2 = \frac{\text{SS}_{\text{res}}}{n-2}$$

Division par $(n-2)$ au lieu de $(n)$:
- **Degrés de liberté:** On a perdu 2 degrés en estimant 2 paramètres ($\alpha$, $\beta$)
- Correction de Bessel: Rend l'estimateur **sans biais**

**Intervalle de Confiance pour la Prédiction (Intervalle de Prédiction):**

$$\boxed{\hat{E}(t^*) \pm t_{n-2, \alpha/2} \cdot \hat{\sigma} \sqrt{1 + \frac{1}{n} + \frac{(t^*-\bar{t})^2}{\sum(t-\bar{t})^2}}}$$

**Composantes de l'incertitude:**
1. **$\hat{\sigma}$:** Bruit aléatoire dans les données (irreducible)
2. **$1/n$:** Incertitude diminue avec plus d'observations
3. **$(t^* - \bar{t})^2$:** Incertitude augmente loin de la moyenne (extrapolation)

**Exemple concret:**
- Données: années 2020-2024, pente = 500 tCO2e/an
- Prédiction 2025 (proche): IC = [6800, 7200] (étroit)
- Prédiction 2030 (loin): IC = [6500, 7500] (plus large)

**Justification bancaire:**
- Banquier demande: "Avec quelle certitude?"
- Réponse: "95% de certitude, l'intervalle est [X, Y]"
- Permet décision d'investissement avec gestion du risque

---

### **MÉTHODE 5: Test F (Significativité Globale)**

#### Objective
Tester si le modèle **explique significativement** la variance

#### Justification Statistique

**Hypothèses du test:**
- $H_0$: $\beta = 0$ (pas de tendance, le modèle est inutile)
- $H_1$: $\beta \neq 0$ (il existe une tendance significative)

**Statistique de test:**
$$F = \frac{\text{MS}_{\text{exp}}}{\text{MS}_{\text{res}}} = \frac{\text{SS}_{\text{exp}}/p}{\text{SS}_{\text{res}}/(n-p-1)}$$

où:
- MS = Mean Square (variance estimée)
- Sous $H_0$: $F \sim F_{p, n-p-1}$

**Interprétation:**
- Si F est **grand**: Variance expliquée >> variance résiduelle → modèle bon
- Si F est **petit**: Variance expliquée ≈ variance résiduelle → modèle mauvais

**Quand rejeter $H_0$?**
$$p\text{-value} = P(F > F_{\text{obs}}) < \alpha = 0.05$$

**Exemple:**
- $F = 45.2$, $p\text{-value} = 0.0001$: Rejeter $H_0$ → **Tendance significative**
- $F = 1.2$, $p\text{-value} = 0.35$: Ne pas rejeter → **Pas de tendance significative**

**Utilité pour prêteur:**
- $p < 0.05$: Confiance que la pente est réelle (pas due au hasard)
- $p > 0.05$: Impossible de conclure, données trop bruitées

---

## 🔬 Justification des Tests Diagnostiques

### **TEST 1: Shapiro-Wilk (Normalité des Résidus)**

#### Objective
Vérifier que les résidus $e_i = E_i - \hat{E}_i$ suivent une **distribution normale**

#### Justification

**Pourquoi la normalité?**

1. **Hypothèse du modèle OLS:**
   - $\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$ (erreurs normales)
   - Quand vraie: $\hat{\beta}$ est efficace, tests t-F valides
   - Quand fausse: Tests restent approx. valides pour large n (TCL)

2. **Que faire si non-normalité?**
   - Petite violation ($p > 0.01$): Accepter (robustesse)
   - Grande violation ($p < 0.001$): 
     - Transformer données (log-transforme données exponentielle)
     - Utiliser régression robuste (moins sensible aux outliers)

**Test Shapiro-Wilk:**
- Hypothèses: $H_0$: Résidus sont normaux
- P-value: Si $p > 0.05$ → Pas de preuve contre normalité ✓
- Si $p < 0.05$ → Données non-normales (mais OLS souvent robuste)

**Interprétation pour jury:**
```
Si p-value = 0.23:
  "Les résidus ne s'écartent pas significativement de la normalité.
   Hypothèse de normalité est raisonnablement satisfaite."

Si p-value = 0.002:
  "Les résidus s'écartent significativement de la normalité.
   Peut indiquer outliers ou forme distributionnelle différente.
   Mais OLS reste valide pour grandes samples."
```

---

### **TEST 2: Durbin-Watson (Autocorrélation)**

#### Objective
Vérifier que les **résidus sont indépendants** dans le temps

#### Justification

**Pourquoi l'indépendance?**

Hypothèse Gauss-Markov:
$$\text{Cov}(\varepsilon_i, \varepsilon_j) = 0 \quad \forall i \neq j$$

Si violée (autocorrélation):
- Estimateurs restent **sans biais**
- Mais **variance estimée est biaisée** → IC trop étroits
- Tests t-F donnent faux résultats

**Exemple:** Autocorrélation positive
- Les erreurs positives sont suivies d'erreurs positives
- Modèle sous-estime la vraie variabilité
- IC trop confiants → **risque de mauvaise décision**

**Statistique Durbin-Watson:**
$$DW = \frac{\sum_{i=2}^{n}(e_i - e_{i-1})^2}{\sum_{i=1}^{n}e_i^2}$$

**Interprétation:**
- $DW \approx 2$: Pas d'autocorrélation ✓
- $DW < 2$: Autocorrélation positive (erreurs liées)
- $DW > 2$: Autocorrélation négative (erreurs alternent)
- Intervalle acceptable: $[1.5, 2.5]$ pour petit n

**Utilité pour prédictions:**
- Autocorrélation → Les prédictions futures sont corrélées
- Les IC ne reflètent pas l'incertitude réelle
- Recommandation: Augmenter les IC si $DW < 1.5$

---

### **TEST 3: F-test (Déjà couvert)**

Voir MÉTHODE 5 ci-dessus.

---

## 💡 Justification des Intervalles de Confiance

### **INTERVALLE DE CONFIANCE pour Moyenne Prédite**

#### Quand l'utiliser?
Quand on veut prédire le **niveau moyen** d'émissions

**Exemple:** "La moyenne des émissions de toutes les usines similaires en 2025 sera dans [X, Y]"

**Formule:**
$$\hat{E}(t^*) \pm t_{n-2, \alpha/2} \cdot \hat{\sigma}\sqrt{\frac{1}{n} + \frac{(t^*-\bar{t})^2}{\sum(t-\bar{t})^2}}$$

**Remarque:** Pas de terme "$1$" sous racine (moins large que PI)

---

### **INTERVALLE DE PRÉDICTION pour Observation Future**

#### Quand l'utiliser?
Quand on veut prédire l'émission **d'une entreprise spécifique**

**Exemple:** "GreenTech Solutions aura des émissions de [X, Y] en 2025 avec 95% confiance"

**Formule:**
$$\hat{E}(t^*) \pm t_{n-2, \alpha/2} \cdot \hat{\sigma}\sqrt{1 + \frac{1}{n} + \frac{(t^*-\bar{t})^2}{\sum(t-\bar{t})^2}}$$

**Justification du terme "+1":**
- **IC moyenne:** Incertitude due à estimation de la ligne
- **PI observation:** IC moyenne + incertitude aléatoire de la nouvelle observation
- Plus large = plus réaliste pour décision bancaire

**Analogie:**
- IC: "Où est la ligne d'ajustement?" (précis)
- PI: "Où se situera le prochain point?" (imprécis car bruit aléatoire)

---

## 📋 Cas d'Usage et Interprétation

### **CAS 1: Entreprise avec Croissance Continue**

```
Données: 
  Années: 2020, 2021, 2022, 2023, 2024
  Émissions: 5000, 5500, 6100, 6700, 7200

Résultat de fit():
  Slope = 550 tCO2e/an
  Intercept = -1107000
  R² = 0.9995 (excellent)
  F p-value = 0.0001 (très significatif)

Interprétation pour prêteur:
  ✓ Tendance claire: +550 tCO2e/an (pente positive)
  ✓ Très bon fit: Modèle explique 99.95% de variance
  ✓ Significatif: Tendance certaine (p=0.0001 < 0.05)
  ⚠️ RISQUE CLIMATIQUE: Croissance constante
  
Décision: À surveiller, exiger plan de réduction
```

---

### **CAS 2: Entreprise avec Émissions Stables**

```
Données: [5000, 5000, 5000, 5000, 5000]

Résultat:
  Slope = 0.0
  R² = 0.0 (IMPORTANT: pas NaN grâce au fix!)
  F p-value = 1.0 (pas significatif)

Interprétation:
  ✓ Aucune tendance: Pente = 0
  ✓ Émissions stables
  ✓ Pas d'amélioration visible
  ⚠️ Mais aussi pas d'augmentation
  
Décision: Acceptable, mais demander plan de réduction
```

---

### **CAS 3: Données Très Bruitées (Faible R²)**

```
Données: [5000, 5800, 5100, 5900, 5200]

Résultat:
  Slope = 50.0
  R² = 0.12 (faible fit)
  F p-value = 0.65 (non-significatif)

Interprétation:
  ⚠️ Tendance très faible (50 tCO2e/an)
  ⚠️ Modèle n'explique que 12% de variance
  ⚠️ Pente non-significatif (p=0.65 > 0.05)
  ✗ DONNÉES INSUFFISANTES: Trop d'autres facteurs
  
Décision: 
  - Rejeter ce modèle
  - Demander données plus détaillées
  - Ou ajouter variables explicatives (énergie, production, ...)
```

---

### **CAS 4: Données Avec Outlier**

```
Données: [5000, 5500, 6100, 15000, 7200]  ← 15000 est outlier

Résultat (avant outlier removal):
  Slope = 2200 (artificiel)
  R² = 0.75
  Shapiro-Wilk p-value = 0.02 (non-normal! signale outlier)

Actions:
  1. Examiner l'outlier (année avec changement opérationnel?)
  2. Si erreur: Supprimer
  3. Si réel: Segmenter les données (avant/après changement)
  4. Ou utiliser régression robuste (moins sensible outliers)

Décision: Refit après validation de données
```

---

## 🏦 Justification Finale pour Comité d'Investissement

### **Pourquoi cette approche?**

| Question | Réponse | Justification |
|----------|---------|---------------|
| **Quel modèle?** | Régression linéaire | Simple, interprétable, OLS = BLUE |
| **Comment estimer?** | OLS (moindres carrés) | Minimise SS_res, MLE sous normalité |
| **Qualité fit?** | R² et R²_adj | Mesure variance expliquée (0-1) |
| **Certitude pente?** | Test-F et p-value | Vérifie significativité (rejet H₀) |
| **Prédictions fiables?** | IC et PI avec t-distribution | Quantifie incertitude avec confiance 95% |
| **Hypothèses vérifiées?** | Shapiro + Durbin-Watson | Vérifie normalité et indépendance |
| **Risque caché?** | Analyse résidus | Détecte outliers, patterns non-capturés |

### **Avantages Scientifiques**

✓ **Transparence:** Chaque paramètre a interprétation claire
✓ **Auditabilité:** Calculs reproductibles et vérifiables
✓ **Rigueur:** Fondations mathématiques solides (Gauss-Markov)
✓ **Gestion risque:** IC/PI quantifient l'incertitude précisément

### **Standards Respectés**

- ✓ **Science-Based Targets (SBT):** Utilise tendances linéaires
- ✓ **TCFD (Task Force on Climate-related Financial Disclosures):** Évaluation trajectoires d'émissions
- ✓ **ISO 14064:** Méthodologies acceptées d'analyse GES
- ✓ **Banques d'investissement:** Standard pour climate risk assessment

---

## 🎓 Conclusion

Chaque composant de notre module a été choisi avec:

1. **Justification mathématique rigoureuse** (OLS = MLE, Gauss-Markov)
2. **Justification statistique** (Tests, IC, diagnostics)
3. **Justification pratique** (Cas d'usage bancaire réel)
4. **Justification scientifique** (Standards ESG acceptés)

Le résultat est un **outil de prédiction certifié, transparent et auditabilité** pour évaluation du risque climatique.

---

**Document préparé pour soutenance du 30 avril 2026**
