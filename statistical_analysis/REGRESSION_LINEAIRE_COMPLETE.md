# 📐 Théorie Complète de la Régression Linéaire

**Document pour Jury de Mathématiques Appliquées**  
Version: 2.0  
Date: 30 avril 2026  
Projet: Calculateur d'Empreinte Carbone - Analyse ESG

---

## 📑 Table des matières

1. [Problématique et Contexte](#problématique-et-contexte)
2. [Formulation Mathématique](#formulation-mathématique)
3. [Estimation OLS](#estimation-ols)
4. [Propriétés des Estimateurs](#propriétés-des-estimateurs)
5. [Mesures de Qualité d'Ajustement](#mesures-de-qualité-dadjustement)
6. [Inférence Statistique](#inférence-statistique)
7. [Diagnostic du Modèle](#diagnostic-du-modèle)
8. [Cas Pathologiques et NaN](#cas-pathologiques-et-nan)
9. [Applications au Projet](#applications-au-projet)

---

## 🎯 Problématique et Contexte

### Objectif

Prédire les émissions futures d'une entreprise à partir d'une série temporelle d'observations historiques.

**Données disponibles:**
- Série temporelle: $(t_1, E_1), (t_2, E_2), \ldots, (t_n, E_n)$
- $t_i$: année ou période $i$
- $E_i$: émissions observées à la période $i$ (en tCO₂e)

### Hypothèse de Base: Linéarité

Nous supposons que la relation entre le temps et les émissions suit un modèle linéaire:

$$\boxed{E_i = \alpha + \beta \cdot t_i + \varepsilon_i, \quad i = 1, 2, \ldots, n}$$

où:
- $\alpha$ = intercept (émissions de base)
- $\beta$ = pente (taux de changement annuel en tCO₂e/an)
- $\varepsilon_i$ = erreur aléatoire à la période $i$

---

## 🧮 Formulation Mathématique

### Notation Matricielle

Le modèle linéaire peut s'écrire sous forme matricielle:

$$\mathbf{E} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$$

où:

$$\mathbf{E} = \begin{pmatrix} E_1 \\ E_2 \\ \vdots \\ E_n \end{pmatrix}, \quad \mathbf{X} = \begin{pmatrix} 1 & t_1 \\ 1 & t_2 \\ \vdots & \vdots \\ 1 & t_n \end{pmatrix}, \quad \boldsymbol{\beta} = \begin{pmatrix} \alpha \\ \beta \end{pmatrix}, \quad \boldsymbol{\varepsilon} = \begin{pmatrix} \varepsilon_1 \\ \varepsilon_2 \\ \vdots \\ \varepsilon_n \end{pmatrix}$$

### Hypothèses Fondamentales

Pour appliquer la théorie OLS, nous posons les hypothèses suivantes (Gauss-Markov):

#### **H1: Linéarité**
Le modèle est linéaire dans les paramètres $(\alpha, \beta)$.

#### **H2: Exogénéité stricte**
$$E[\varepsilon_i | \mathbf{X}] = 0 \quad \forall i$$

Cela implique que les erreurs ne sont pas corrélées avec les variables explicatives.

#### **H3: Pas de multicolinéarité**
La matrice $\mathbf{X}^T\mathbf{X}$ est inversible (rang plein).

En régression simple, cela signifie: $\sum_{i=1}^n (t_i - \bar{t})^2 \neq 0$

#### **H4: Homoscédasticité**
$$\text{Var}(\varepsilon_i | \mathbf{X}) = \sigma^2 \quad \forall i$$

Les erreurs ont une variance constante.

#### **H5: Non-autocorrélation**
$$\text{Cov}(\varepsilon_i, \varepsilon_j | \mathbf{X}) = 0 \quad \forall i \neq j$$

Les erreurs ne sont pas corrélées entre elles.

#### **H6: Normalité (optionnel)**
$$\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$$

Nécessaire pour les tests d'hypothèse, mais pas pour la consistance des estimateurs.

---

## 📊 Estimation OLS

### Principe des Moindres Carrés

L'estimateur OLS minimise la somme des carrés des résidus:

$$\boxed{(\hat{\alpha}, \hat{\beta}) = \arg\min_{\alpha, \beta} \sum_{i=1}^{n} (E_i - \alpha - \beta \cdot t_i)^2}$$

### Dérivation Analytique

Soit $L(\alpha, \beta) = \sum_{i=1}^{n} (E_i - \alpha - \beta \cdot t_i)^2$ la fonction de coût.

Les conditions de premier ordre (FOC) sont:

$$\frac{\partial L}{\partial \alpha} = -2\sum_{i=1}^{n} (E_i - \alpha - \beta \cdot t_i) = 0 \quad \text{...(1)}$$

$$\frac{\partial L}{\partial \beta} = -2\sum_{i=1}^{n} t_i(E_i - \alpha - \beta \cdot t_i) = 0 \quad \text{...(2)}$$

De l'équation (1):
$$\sum_{i=1}^{n} E_i = n\alpha + \beta \sum_{i=1}^{n} t_i$$

$$n\bar{E} = n\alpha + \beta \cdot n\bar{t}$$

$$\boxed{\hat{\alpha} = \bar{E} - \hat{\beta} \cdot \bar{t}} \quad \text{...(3)}$$

De l'équation (2) avec substitution de (3):
$$\sum_{i=1}^{n} t_i E_i = (\bar{E} - \hat{\beta}\bar{t}) \sum_{i=1}^{n} t_i + \hat{\beta}\sum_{i=1}^{n} t_i^2$$

Après simplification (voir annexe):

$$\boxed{\hat{\beta} = \frac{\sum_{i=1}^{n}(t_i - \bar{t})(E_i - \bar{E})}{\sum_{i=1}^{n}(t_i - \bar{t})^2}} \quad \text{...(4)}$$

### Formules Équivalentes

La pente peut aussi s'écrire:

$$\hat{\beta} = \frac{\text{Cov}(t, E)}{\text{Var}(t)} = \frac{S_{tE}}{S_{tt}}$$

où $S_{tt} = \sum(t_i - \bar{t})^2$ et $S_{tE} = \sum(t_i - \bar{t})(E_i - \bar{E})$.

---

## 🎁 Propriétés des Estimateurs

### Théorème de Gauss-Markov

**Sous les hypothèses H1-H5**, les estimateurs OLS $\hat{\beta}$ et $\hat{\alpha}$ satisfont:

#### 1. **Non-biais**
$$E[\hat{\beta}] = \beta \quad \text{et} \quad E[\hat{\alpha}] = \alpha$$

**Démonstration:** Par linéarité de l'espérance et exogénéité (H2).

#### 2. **Variance minimale (BLUE)**

$$\text{Var}(\hat{\beta}) = \frac{\sigma^2}{\sum_{i=1}^{n}(t_i - \bar{t})^2} = \frac{\sigma^2}{S_{tt}}$$

$$\text{Var}(\hat{\alpha}) = \sigma^2 \left(\frac{1}{n} + \frac{\bar{t}^2}{S_{tt}}\right)$$

Les estimateurs OLS ont la variance minimale parmi tous les estimateurs linéaires sans biais (BLUE = Best Linear Unbiased Estimator).

#### 3. **Consistance**

$$\hat{\beta} \xrightarrow{p} \beta \quad \text{quand} \quad n \to \infty$$

$$\hat{\alpha} \xrightarrow{p} \alpha \quad \text{quand} \quad n \to \infty$$

(p = convergence en probabilité)

#### 4. **Normalité Asymptotique**

Sous H6 (normalité des erreurs):

$$\hat{\beta} \sim \mathcal{N}\left(\beta, \frac{\sigma^2}{S_{tt}}\right)$$

$$\hat{\alpha} \sim \mathcal{N}\left(\alpha, \sigma^2\left(\frac{1}{n} + \frac{\bar{t}^2}{S_{tt}}\right)\right)$$

---

## 📈 Mesures de Qualité d'Ajustement

### 1. Coefficient de Détermination $R^2$

#### Définition

Le coefficient $R^2$ mesure la fraction de la variance totale expliquée par le modèle:

$$\boxed{R^2 = \frac{\text{SS}_{\text{exp}}}{\text{SS}_{\text{tot}}} = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}}$$

#### Décomposition de la Variance (ANOVA)

$$\underbrace{\sum_{i=1}^{n}(E_i - \bar{E})^2}_{\text{SS}_{\text{tot}}} = \underbrace{\sum_{i=1}^{n}(\hat{E}_i - \bar{E})^2}_{\text{SS}_{\text{exp}}} + \underbrace{\sum_{i=1}^{n}(E_i - \hat{E}_i)^2}_{\text{SS}_{\text{res}}}$$

où:
- $\text{SS}_{\text{tot}} = S_{EE} = \sum(E_i - \bar{E})^2$ : somme totale des carrés (variation totale)
- $\text{SS}_{\text{exp}} = \sum(\hat{E}_i - \bar{E})^2$ : somme expliquée (variation expliquée par le modèle)
- $\text{SS}_{\text{res}} = \sum(E_i - \hat{E}_i)^2$ : somme des carrés résiduelle (variation inexpliquée)

#### Propriétés

- $0 \leq R^2 \leq 1$ **en général**
- $R^2 = 0$: le modèle n'explique aucune variance
- $R^2 = 1$: ajustement parfait aux données
- **IMPORTANT**: $R^2 \geq 0$ en régression avec constante

#### Relation avec la Corrélation

En régression simple:

$$R^2 = r^2$$

où $r = \frac{S_{tE}}{\sqrt{S_{tt} \cdot S_{EE}}}$ est le coefficient de corrélation de Pearson.

### 2. Coefficient de Détermination Ajusté ($R^2_{\text{adj}}$)

Le $R^2$ augmente mécaniquement avec le nombre de variables explicatives. Pour corriger ce biais, on utilise le $R^2$ ajusté:

$$\boxed{R^2_{\text{adj}} = 1 - \frac{\text{SS}_{\text{res}}/(n-k-1)}{\text{SS}_{\text{tot}}/(n-1)} = 1 - (1-R^2)\frac{n-1}{n-k-1}}$$

où $k$ est le nombre de variables explicatives ($k=1$ en régression simple).

**Propriétés:**
- $R^2_{\text{adj}} < R^2$ (toujours)
- $R^2_{\text{adj}}$ peut être négatif si le modèle ajuste mal
- Préféré pour comparer des modèles avec nombre différent de variables

### 3. Erreur Standard de l'Estimation

L'erreur standard résiduelle estime l'écart-type du terme d'erreur:

$$\hat{\sigma}^2 = \frac{\text{SS}_{\text{res}}}{n-2}$$

$$\boxed{\hat{\sigma} = \sqrt{\frac{\sum_{i=1}^{n}(E_i - \hat{E}_i)^2}{n-2}}}$$

La division par $n-2$ (au lieu de $n$) rend cet estimateur sans biais (correction des degrés de liberté).

**Degrés de liberté:** $n - 2 = n - k - 1$ où $k=1$ (nombre de paramètres estimés = 2: $\alpha$ et $\beta$).

---

## 🔬 Inférence Statistique

### 1. Test de Significativité de la Pente

**Hypothèses du test:**
- $H_0: \beta = 0$ (pas de tendance)
- $H_1: \beta \neq 0$ (présence d'une tendance)

**Statistique de test:**

$$\boxed{t = \frac{\hat{\beta} - 0}{\text{SE}(\hat{\beta})} = \frac{\hat{\beta}}{\hat{\sigma}/\sqrt{S_{tt}}} \sim t_{n-2}}$$

sous $H_0$, suit une distribution $t$ de Student avec $n-2$ degrés de liberté.

**Erreur standard de la pente:**

$$\text{SE}(\hat{\beta}) = \frac{\hat{\sigma}}{\sqrt{S_{tt}}}$$

**Région critique (test bilatéral à seuil $\alpha$):**

Rejecter $H_0$ si $|t| > t_{n-2, \alpha/2}$

**P-valeur:** $p = 2 \cdot P(|T| > |t_{\text{obs}}|)$ où $T \sim t_{n-2}$

### 2. Test de Significativité Globale (F-test)

**Hypothèses:**
- $H_0: \beta = 0$ (le modèle n'améliore pas la prédiction)
- $H_1: \beta \neq 0$

**Statistique de test:**

$$\boxed{F = \frac{\text{SS}_{\text{exp}}/k}{\text{SS}_{\text{res}}/(n-k-1)} = \frac{\text{MS}_{\text{exp}}}{\text{MS}_{\text{res}}} \sim F_{k, n-k-1}}$$

où:
- MS = Mean Square (variance)
- $k = 1$ en régression simple

En régression simple: $F = t^2$ (équivalence du test t avec le F-test)

**Table ANOVA:**

| Source | SS | df | MS | F |
|--------|----|----|----|----|
| Regression | $\text{SS}_{\text{exp}}$ | $k$ | $\text{MS}_{\text{exp}}$ | $\text{MS}_{\text{exp}}/\text{MS}_{\text{res}}$ |
| Residual | $\text{SS}_{\text{res}}$ | $n-k-1$ | $\text{MS}_{\text{res}}$ | |
| Total | $\text{SS}_{\text{tot}}$ | $n-1$ | | |

### 3. Intervalles de Confiance

#### IC pour la pente

Avec confiance $1-\alpha$:

$$\boxed{\hat{\beta} \pm t_{n-2, \alpha/2} \cdot \text{SE}(\hat{\beta})}$$

#### IC pour l'intercept

$$\boxed{\hat{\alpha} \pm t_{n-2, \alpha/2} \cdot \text{SE}(\hat{\alpha})}$$

où $\text{SE}(\hat{\alpha}) = \hat{\sigma}\sqrt{\frac{1}{n} + \frac{\bar{t}^2}{S_{tt}}}$

#### IC pour la moyenne prédite

Pour une prédiction au point $t^*$:

$$\boxed{\hat{E}(t^*) \pm t_{n-2, \alpha/2} \cdot \hat{\sigma}\sqrt{\frac{1}{n} + \frac{(t^* - \bar{t})^2}{S_{tt}}}}$$

Cet intervalle est plus étroit que l'intervalle de prédiction.

#### IC pour une observation future (intervalle de prédiction)

$$\boxed{\hat{E}(t^*) \pm t_{n-2, \alpha/2} \cdot \hat{\sigma}\sqrt{1 + \frac{1}{n} + \frac{(t^* - \bar{t})^2}{S_{tt}}}}$$

La présence du terme $1$ dans la racine le rend plus large (incertitude additionnelle).

---

## 🔍 Diagnostic du Modèle

### 1. Résidus et Leur Analyse

Les résidus sont définis comme:

$$e_i = E_i - \hat{E}_i = E_i - (\hat{\alpha} + \hat{\beta}t_i)$$

**Propriétés des résidus:**
- $\sum e_i = 0$ (par construction)
- $\sum e_i \cdot t_i = 0$ (propriété OLS)
- $E[e_i] \approx 0$ si le modèle est bien spécifié

### 2. Test de Normalité (Shapiro-Wilk)

**Hypothèses:**
- $H_0$: Les résidus suivent une distribution normale
- $H_1$: Les résidus ne suivent pas une distribution normale

**Statistique:**

$$W = \frac{\left(\sum_{i=1}^{n} a_i e_{(i)}\right)^2}{\sum_{i=1}^{n}(e_i - \bar{e})^2}$$

où $e_{(i)}$ sont les résidus ordonnés et $a_i$ sont des coefficients tabulés.

**Interprétation:**
- $W$ proche de 1: données normales
- $p$-value > 0.05: ne pas rejeter la normalité

### 3. Test d'Hétéroscédasticité (Breusch-Pagan)

**Hypothèses:**
- $H_0$: Homoscédasticité ($\text{Var}(\varepsilon_i)$ constante)
- $H_1$: Hétéroscédasticité

**Procédure:**
1. Régresser $e_i^2$ sur la variable explicative $t_i$
2. Calculer la statistique: $BP = n \cdot R^2_{\text{aux}}$
3. Sous $H_0$: $BP \sim \chi^2_1$

**Interprétation:**
- $p$-value > 0.05: ne pas rejeter l'homoscédasticité

### 4. Test d'Autocorrélation (Durbin-Watson)

**Hypothèses:**
- $H_0$: Pas d'autocorrélation
- $H_1$: Autocorrélation d'ordre 1

**Statistique:**

$$\boxed{DW = \frac{\sum_{i=2}^{n}(e_i - e_{i-1})^2}{\sum_{i=1}^{n}e_i^2}}$$

**Interprétation:**
- $DW \approx 2$: pas d'autocorrélation
- $DW \approx 0$: autocorrélation positive
- $DW \approx 4$: autocorrélation négative

### 5. Diagnostic Graphique

**Graphiques essentiels:**

1. **Scatter plot** : Points de données + ligne de régression
2. **Résidus vs Valeurs prédites**: Vérifier l'homoscédasticité
3. **Q-Q plot** : Vérifier la normalité
4. **Résidus vs Ordre** : Vérifier l'indépendance (pas de patterns)

---

## ⚠️ Cas Pathologiques et NaN

### **PROBLÈME: Pourquoi $R^2 = \text{NaN}$ ?**

#### Cas 1: Variable dépendante constante

**Condition:** $\text{SS}_{\text{tot}} = 0$ (toutes les valeurs $E_i$ sont identiques)

**Analyse:**

$$R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = 1 - \frac{0}{0} \quad \text{(indéterminée)}$$

C'est une forme indéterminée $0/0$ qui produit NaN en informatique.

**Raison statistique:** Si la variable dépendante n'a aucune variation, il n'y a rien à expliquer. Le concept même de $R^2$ n'a plus de sens.

**Solution:** Par convention, on pose $R^2 = 0$ (le modèle n'explique aucune variance car il n'y a aucune variance à expliquer).

#### Cas 2: Variable indépendante constante

**Condition:** $S_{tt} = \sum(t_i - \bar{t})^2 = 0$ (toutes les années sont identiques)

**Analyse:** La pente devient:

$$\hat{\beta} = \frac{\text{Cov}(t, E)}{\text{Var}(t)} = \frac{C}{0} \quad \text{(division par zéro)}$$

Impossible d'estimer le modèle.

**Solution:** Vérifier que les données temporelles ont une variation suffisante.

#### Cas 3: Colinéarité parfaite (régression multiple)

**Condition:** Deux ou plus variables explicatives sont parfaitement corrélées.

**Analyse:** La matrice $\mathbf{X}^T\mathbf{X}$ devient singulière:

$$\det(\mathbf{X}^T\mathbf{X}) = 0 \quad \Rightarrow \quad (\mathbf{X}^T\mathbf{X})^{-1} \text{ n'existe pas}$$

**Solution:** Supprimer une des variables colinéaires.

#### Cas 4: Données manquantes ou mauvaises

**Problèmes possibles:**
- Valeurs NaN dans les données d'entrée
- Valeurs infinies
- Codage manuel (exemple: valeurs numériques représentant des catégories)

**Solution:** Nettoyer et valider les données avant l'ajustement.

### **Traitement Implémenté dans le Code**

```python
# Vérification de la variation en x
x_var = np.sum((x_array - x_mean) ** 2)
if x_var < 1e-10:  # essentiellement zéro
    raise ValueError("Variable indépendante constante")

# Vérification de la variation en y
y_var = np.sum((y_array - y_mean) ** 2)
if y_var < 1e-10:
    print("[WARNING] Variable dépendante constante")
    r_squared = 0.0  # par convention

# Calcul sûr de R²
if ss_tot < 1e-10:  # SS_tot ≈ 0
    r_squared = 0.0  # convention
else:
    r_squared = 1 - (ss_res / ss_tot)
```

---

## 💼 Applications au Projet

### Exemple Concret: Entreprise XYZ

**Données historiques:**
```
Année:     2020  2021  2022  2023
Émissions: 5000  5500  6100  6800  (tCO2e)
```

**Étape 1: Calcul des statistiques descriptives**

$$\bar{t} = \frac{2020+2021+2022+2023}{4} = 2021.5$$

$$\bar{E} = \frac{5000+5500+6100+6800}{4} = 5875$$

**Étape 2: Calcul de la pente**

$$S_{tt} = (2020-2021.5)^2 + \cdots + (2023-2021.5)^2 = 5$$

$$S_{tE} = (2020-2021.5)(5000-5875) + \cdots = 2750$$

$$\hat{\beta} = \frac{2750}{5} = 550 \text{ tCO2e/an}$$

**Étape 3: Calcul de l'intercept**

$$\hat{\alpha} = 5875 - 550 \times 2021.5 = -1110075$$

**Étape 4: Calcul de $R^2$**

Valeurs prédites: $\hat{E}_i = -1110075 + 550 \cdot t_i$

$$\text{SS}_{\text{tot}} = \sum(E_i - 5875)^2 \approx 1550000$$

$$\text{SS}_{\text{res}} = \sum(E_i - \hat{E}_i)^2 \approx 250000$$

$$R^2 = 1 - \frac{250000}{1550000} \approx 0.839$$

**Interprétation:** Le modèle explique 83.9% de la variation des émissions, ce qui indique un excellent ajustement.

### Recommandations pour le Projet

1. **Toujours vérifier les hypothèses** avant d'utiliser le modèle
2. **Signaler les avertissements** (comme le NaN) plutôt que d'ignorer silencieusement
3. **Fournir les tests diagnostiques** (Shapiro, Durbin-Watson) aux utilisateurs
4. **Documenter les limitations** du modèle linéaire

---

## 📚 Références Mathématiques

- **Équations normales:** Dérivation des estimateurs OLS
- **Théorème de Gauss-Markov:** Optimalité des estimateurs OLS
- **Distributions d'échantillonnage:** Inférence statistique basée sur $t$ et $F$
- **ANOVA:** Décomposition de la variance
- **Tests statistiques:** Shapiro-Wilk, Breusch-Pagan, Durbin-Watson

---

## Annexe: Simplifications Algébriques

### Simplification de l'équation (2)

À partir de:
$$\sum_{i=1}^{n} t_i(E_i - \alpha - \beta \cdot t_i) = 0$$

En substituant $\alpha = \bar{E} - \beta\bar{t}$:

$$\sum t_i E_i - \sum t_i(\bar{E} - \beta\bar{t}) - \sum \beta t_i^2 = 0$$

$$\sum t_i E_i - \bar{E}\sum t_i + \beta\bar{t}\sum t_i - \beta\sum t_i^2 = 0$$

$$\sum t_i E_i - n\bar{E}\bar{t} + \beta n\bar{t}^2 - \beta\sum t_i^2 = 0$$

$$\sum t_i E_i - n\bar{E}\bar{t} = \beta\left(\sum t_i^2 - n\bar{t}^2\right)$$

$$\boxed{\hat{\beta} = \frac{\sum t_i E_i - n\bar{E}\bar{t}}{\sum t_i^2 - n\bar{t}^2}}$$

Cette forme est équivalente à la formule (4).

---

**Document préparé pour la soutenance du 30 avril 2026**
