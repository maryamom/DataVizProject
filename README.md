---
title: Data Visualization Intelligente
emoji: 📊
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: "1.40.0"
app_file: app.py
pinned: false
---

# 📊 Data Visualization Intelligente

Application web intelligente de data visualization pilotée par LLM pour le Master 2 BDIA (Big Data & Intelligence Artificielle).

## Description

L'application permet de répondre automatiquement à une problématique métier en :
1. Prenant en entrée une problématique textuelle et un dataset tabulaire (CSV ou Hugging Face)
2. Générant automatiquement 3 propositions de visualisations différentes via LLM, chacune justifiée et conforme aux bonnes pratiques
3. Permettant à l'utilisateur de sélectionner une proposition
4. Générant la visualisation finale formatée avec export PNG

## Fonctionnalités

- **Entrée** : Problématique textuelle + dataset (CSV upload ou Hugging Face)
- **Génération LLM** : 3 propositions de visualisations justifiées (scaffolding)
- **Interaction** : Sélection d'une proposition → visualisation finale
- **Export** : Téléchargement au format PNG

## Installation

### Prérequis

- Python 3.10+
- [Poetry](https://python-poetry.org/) (gestionnaire de dépendances)

### Étapes

```bash
# Cloner le dépôt
git clone <url-du-repo>
cd projetFINAL

# Installer les dépendances avec Poetry
poetry install

# Copier le fichier d'environnement et configurer la clé API
cp .env.example .env
# Éditer .env et ajouter votre OPENAI_API_KEY
```

### Configuration

Créer un fichier `.env` à la racine :

```
GEMINI_API_KEY=votre-cle-gemini
# Clé gratuite : https://aistudio.google.com/app/apikey
GEMINI_MODEL=gemini-2.0-flash  # optionnel, défaut: gemini-2.0-flash
```

## Lancement

```bash
# Avec Poetry
poetry run streamlit run app.py

# Ou après activation du venv
streamlit run app.py
```

L'application sera accessible sur [http://localhost:8501](http://localhost:8501).

## Déploiement sur Hugging Face Spaces

**Application en ligne :** [https://huggingface.co/spaces/MriemOmrani/DataViz](https://huggingface.co/spaces/MriemOmrani/DataViz)

1. Créer un nouvel espace sur [Hugging Face Spaces](https://huggingface.co/spaces)
2. Choisir le SDK **Streamlit**
3. Cloner ce dépôt et pousser les fichiers
4. Ajouter les secrets :
   - `GEMINI_API_KEY` : votre clé API Gemini (https://aistudio.google.com/app/apikey)
5. Le fichier `app.py` à la racine sert de point d'entrée

Exemple de structure pour HF Spaces :
- `app.py` (entrée Streamlit)
- `pyproject.toml` ou `requirements.txt`
- Dossier `src/` avec le code

## Exemples d'utilisation

### Exemple 1 : Spotify (musique et ventes)

- **Problématique** : "Quel style de musique maximise le nombre de ventes pour une entreprise de production musicale ?"
- **Dataset** : `maharshipandya/spotify-tracks-dataset` (Hugging Face)
- Colonnes clés : `track_genre`, `popularity` (proxy ventes), etc.

### Exemple 2 : Logements Paris

- **Problématique** : "Quels facteurs influencent le prix des logements à Paris ?"
- **Dataset** : CSV avec colonnes (prix, superficie, quartier, etc.)

### Exemple 3 : Autre dataset

Uploadez tout fichier CSV et formulez votre problématique métier.

## Structure du projet

```
projetFINAL/
├── src/
│   └── data_viz_app/
│       ├── __init__.py
│       ├── app.py           # Application Streamlit
│       ├── data_loader.py   # Chargement CSV / Hugging Face
│       ├── llm_client.py    # Client LLM (propositions)
│       └── visualizations.py # Génération des graphiques
├── tests/
│   └── test_visualizations.py
├── app.py                   # Point d'entrée Streamlit
├── pyproject.toml
├── .env.example
├── README.md
└── LICENSE
```

## Bonnes pratiques appliquées

- Data-ink ratio maximal
- Évitement du chartjunk
- Choix du type de graphique adapté aux données
- Lisibilité (titres, axes, légendes)
- Palette de couleurs cohérente

## Technologies

- **Frontend/UI** : Streamlit
- **LLM** : Google Gemini (gemini-2.0-flash par défaut)
- **Visualisation** : Plotly
- **Données** : Pandas, Hugging Face Datasets

## Licence

MIT - Voir [LICENSE](LICENSE)
"# DataVizProject" 
