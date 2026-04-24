# Guide d'Utilisation des 3 Cas d'Étude dans le Dashboard

## 📖 Vue d'Ensemble

Ce guide explique comment utiliser les 3 cas d'étude pour :
- **Former** les utilisateurs du dashboard
- **Tester** le système d'évaluation
- **Démontrer** les 3 niveaux de recommandation
- **Valider** la logique métier

---

## 🚀 Avant de Démarrer

### Structure du Dossier
```
etudes_de_cas/
│
├── README.md (ce fichier - guide principal)
├── COMPARAISON_3_CAS.md (comparatif détaillé)
│
├── 1_ACCEPTABLE_GreenTech_Solutions/
│   ├── cas_1.md (description complète)
│   └── donnees_cas1.json (données)
│
├── 2_ACCEPTABLE_CONDITIONS_EnerCorp/
│   ├── cas_2.md (conditions strictes)
│   └── donnees_cas2.json (données avec scenario)
│
└── 3_REFUS_TOTAL_HeavyManufacturing/
    ├── cas_3.md (analyse critique)
    └── donnees_cas3.json (données + risques)
```

---

## 💻 Procédure: Saisir un Cas dans le Dashboard

### Cas 1: GreenTech Solutions (5 minutes)

#### Étape 1: Créer l'Évaluation
1. Ouvrir le dashboard `python -m streamlit run pfe_project/dashboard.py`
2. Dans la **barre latérale**, sous "Configuration de l'Entreprise":
   - **Nom**: `GreenTech Solutions SA`
   - **Revenu annuel**: `150` MDT
   - **Année**: `2024`
3. Cliquer **"Créer une nouvelle évaluation"**

#### Étape 2: Onglet 2 - Nos Opérations (Directes)
**Section Combustibles Fossiles:**
- Type: Gaz naturel
- Quantité: 5000
- Installation: Siège principal
- Mois: 12
- Ajouter ✅

**Section Combustibles Fossiles (2):**
- Type: Essence
- Quantité: 100
- Installation: Siège principal
- Mois: 6
- Ajouter ✅

#### Étape 3: Onglet 3 - Énergie Achetée
**Électricité (source renouvelable):**
- Source: Renouvelable
- Quantité: 150000
- Installation: Siège principal
- Mois: 12
- Ajouter ✅

**Électricité (source réseau):**
- Source: Réseau moyen
- Quantité: 50000
- Installation: Siège principal
- Mois: 12
- Ajouter ✅

#### Étape 4: Onglet 4 - Chaîne de Valeur

**Eau:**
- Type: Approvisionnement
- Quantité: 1000
- Installation: Siège principal
- Ajouter ✅

**Déchets:**
- Type: Recyclage
- Quantité: 2000
- Installation: Siège principal
- Ajouter ✅

**Voyages:**
- Type: Vol court
- Distance: 5000
- Lieu: Siège principal
- Ajouter ✅

#### Étape 5: Consultez Onglet 5 - Résultats
**Résultat attendu:**
```
✅ Émissions Totales: ~10,900 kg CO2e
✅ Intensité Carbone: ~72.8 kg CO2e/$1M
✅ Risque: 🟢 FAIBLE
✅ Recommandation: 🟢 INVESTISSEMENT RECOMMANDÉ
```

**Observations clés:**
- 75% d'électricité renouvelable (données)
- Faible empreinte directe
- Risque climatique minimal
- Excellent profile ESG

---

### Cas 2: EnerCorp Industries (10 minutes)

#### Étape 1: Créer l'Évaluation
1. **Nouveau calcul** (nouvelle session ou refresh)
2. Dans la **barre latérale**:
   - **Nom**: `EnerCorp Industries SARL`
   - **Revenu annuel**: `400` MDT
   - **Année**: `2024`
3. Cliquer **"Créer une nouvelle évaluation"**

#### Étape 2: Onglet 2 - Nos Opérations (Directes)

**Combustibles Fossiles (Gaz naturel):**
- Type: Gaz naturel
- Quantité: 500000 (important!)
- Installation: Centrale Sfax
- Ajouter ✅

**Combustibles Fossiles (Charbon):**
- Type: Charbon
- Quantité: 50000
- Installation: Centrale Sfax
- Ajouter ✅

**Combustibles Fossiles (Diesel):**
- Type: Diesel
- Quantité: 2000
- Installation: Flotte transport
- Ajouter ✅

**Émissions Fugitives:**
- Quantité: 500 kg ⚠️ Important - source majeure!
- Installation: Système climatisation
- Ajouter ✅

#### Étape 3: Onglet 3 - Énergie Achetée

**Électricité (Thermique):**
- Source: Thermique
- Quantité: 150000
- Installation: Siège
- Ajouter ✅

**Électricité (Renouvelable):**
- Source: Renouvelable
- Quantité: 100000
- Installation: Siège
- Ajouter ✅

#### Étape 4: Onglet 4 - Chaîne de Valeur

**Eau:**
- Type: Approvisionnement
- Quantité: 5000
- Ajouter ✅

**Déchets:**
- Type: Décharge (pas recyclage!)
- Quantité: 10000
- Ajouter ✅

**Voyages:**
- Type: Vol long
- Distance: 20000
- Ajouter ✅

#### Étape 5: Consultez Onglet 5 - Résultats
**Résultat attendu:**
```
⚠️ Émissions Totales: ~500,000-550,000 kg CO2e
⚠️ Intensité Carbone: ~125-137 kg CO2e/$1M
⚠️ Risque: 🟡 MODÉRÉ
⚠️ Recommandation: 🟡 ACCEPTABLE SOUS CONDITIONS
```

**Observations clés:**
- Fuites réfrigération représentent ~60% Portée 1
- Mix énergétique < 50% renouvelable
- À la limite du seuil acceptable
- Nécessite plan de transition

**Points à noter:**
- Observer le graphique Portée 1 (dominante)
- Voir l'impact des fuites
- Comprendre le risque modéré

---

### Cas 3: HeavyManufacturing Steel (15 minutes)

#### Étape 1: Créer l'Évaluation
1. **Nouveau calcul**
2. Dans la **barre latérale**:
   - **Nom**: `HeavyManufacturing Steel Corp`
   - **Revenu annuel**: `600` MDT
   - **Année**: `2024`
3. Cliquer **"Créer une nouvelle évaluation"**

#### Étape 2: Onglet 2 - Nos Opérations (Directes)

Ajoutez progressivement pour voir l'impact:

**Combustible 1 - Charbon (MASSIF):**
- Type: Charbon
- Quantité: 2000000 ⚠️ ÉNORME
- Installation: Haut-fourneau 1
- Ajouter ✅

**Combustible 2 - Gaz naturel:**
- Type: Gaz naturel
- Quantité: 800000
- Installation: Fours à arc
- Ajouter ✅

**Remarque:** À ce stade, observez déjà l'augmentation drastique!

**Combustible 3 - Diesel:**
- Type: Diesel
- Quantité: 10000
- Installation: Flotte
- Ajouter ✅

**Émissions Fugitives:**
- Quantité: 2000 kg ⚠️ TRÈS ÉLEVÉ
- Installation: Système refroidissement
- Ajouter ✅

#### Étape 3: Onglet 3 - Énergie Achetée

**Électricité (Charbon):**
- Source: Charbon
- Quantité: 500000
- Installation: Usine
- Ajouter ✅

**Électricité (Thermique):**
- Source: Thermique
- Quantité: 300000
- Installation: Usine
- Ajouter ✅

#### Étape 4: Onglet 4 - Chaîne de Valeur

**Eau:**
- Quantité: 50000 (industrielle massive)
- Ajouter ✅

**Déchets:**
- Type: Décharge
- Quantité: 100000
- Ajouter ✅

**Voyages:**
- Type: Vol long
- Distance: 30000
- Ajouter ✅

#### Étape 5: Consultez Onglet 5 - Résultats
**Résultat attendu:**
```
🔴 Émissions Totales: ~12,000,000+ kg CO2e
🔴 Intensité Carbone: ~2,000+ kg CO2e/$1M
🔴 Risque: 🔴 ÉLEVÉ
🔴 Recommandation: 🔴 RISQUE CLIMATIQUE ÉLEVÉ
```

**Observations critiques:**
- Émissions 1000+ fois plus que GreenTech!
- Intensité carbone 4x au-dessus seuil
- Portée 1 = 97.5% du total (fossiles)
- Zéro énergies renouvelables
- REFUS TOTAL d'investissement

**À noter pour formation:**
- Le graphique est complètement dominé par Portée 1
- Voir le risque "ÉLEVÉ" en rouge
- S'attarder sur le message de refus

---

## 📊 Comparaison Visuelle en Dashboard

### Côte à Côte (3 sessions simultanées)
```
GreenTech          EnerCorp            HeavyManufacturing
═════════════════  ═════════════════  ═════════════════
🟢 10.9K CO2e      🟡 514K CO2e        🔴 12.1M CO2e
🟢 72.8 (kg/M)     🟡 128.6 (kg/M)    🔴 2,022 (kg/M)
🟢 FAIBLE          🟡 MODÉRÉ          🔴 ÉLEVÉ
🟢 INVESTI         🟡 CONDITIONS      🔴 REFUS
```

---

## 🎓 Scénarios d'Utilisation Pédagogiques

### 1. Formation Utilisateurs Novices
**Objectif:** Comprendre les 3 niveaux de risque

**Procédure:**
1. Démarrer avec Cas 1 (succès/compréhension)
2. Progresser vers Cas 2 (complexité)
3. Expérimenter Cas 3 (cas d'école - refus!)

**Temps:** 45 minutes
**Output:** Compréhension des thresholds

### 2. Validation du Système
**Objectif:** Vérifier que les calculs/recommandations sont corrects

**Procédure:**
1. Saisir chaque cas exactement
2. Comparer résultats vs fichiers .md
3. Valider messages de recommandation

**Temps:** 30 minutes
**Output:** Validation QA

### 3. Démonstration Exécutive
**Objectif:** Montrer la logique d'investissement durable

**Procédure:**
1. Cas 1: Montrer succès (2 min)
2. Cas 2: Montrer conditions d'impact (3 min)
3. Cas 3: Expliquer refus responsable (3 min)

**Temps:** 10 min (rapide & impactant)
**Output:** Buy-in direction/stakeholders

---

## ⚙️ Intégration Technique (Optionnel)

### Créer un Script Python d'Importation

```python
# load_case_study.py
import json
from pathlib import Path
from pfe_project.models import CompanyData, Activity
from pfe_project.calculator import CarbonFootprintCalculator

def load_case_study(case_number: int):
    """Charge un cas d'étude et retourne le calculateur."""
    
    cases = {
        1: "1_ACCEPTABLE_GreenTech_Solutions/donnees_cas1.json",
        2: "2_ACCEPTABLE_CONDITIONS_EnerCorp/donnees_cas2.json",
        3: "3_REFUS_TOTAL_HeavyManufacturing/donnees_cas3.json"
    }
    
    if case_number not in cases:
        raise ValueError("Case 1-3 only")
    
    # Charger JSON
    path = Path(__file__).parent / "etudes_de_cas" / cases[case_number]
    with open(path) as f:
        data = json.load(f)
    
    # Créer CompanyData
    company = CompanyData(name=data["company"]["name"])
    
    # Ajouter activities (simplifié)
    # ... implémentation détaillée selon modèles
    
    return CarbonFootprintCalculator(company)

# Usage
calc = load_case_study(1)  # Load GreenTech
```

---

## 📋 Checklist de Vérification

Quand vous terminez un cas, vérifier:

- [ ] Émissions totales correspondent
- [ ] Intensité carbone ±2% de attendu
- [ ] Classification risque correct (VERT/JAUNE/ROUGE)
- [ ] Recommandation correspond au cas
- [ ] Graphiques montrent bonne répartition Portées
- [ ] Messages d'investissement appropriés

---

## 🆘 Troubleshooting

### Les émissions sont beaucoup plus élevées que prévues
- Vérifier les unités (kWh vs tonnes)
- Vérifier les quantités saisies
- Vérifier les facteurs d'émission utilisés

### La recommandation est différente
- Vérifier formule intensité carbone
- Vérifier seuils de risque (100/500)
- Vérifier revenu saisi

### Les graphiques ne montrent rien
- Ajouter des activités à chaque onglet
- Onglet 5 affiche que si activités présentes
- Passer par onglets 2-4 avant onglet 5

---

## 📱 Cas Mobiles (Futur)

Ces cas peuvent servir de base pour:
- Application mobile
- API REST
- Export PDF/Excel
- Dashboard B2B

---

## 🎯 Prochaines Étapes

1. **Tester les 3 cas** dans le dashboard
2. **Valider les résultats** vs documentation
3. **Former utilisateurs** avec Cas 1→2→3
4. **Documenter** feedbacks utilisateurs
5. **Itérer** logique si nécessaire

---

*Guide créé pour faciliter utilisation des cas d'étude - Last Update: 2026*
