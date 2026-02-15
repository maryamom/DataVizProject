# Déploiement sur Hugging Face Spaces

Guide pas à pas pour déployer l'application Data Visualization Intelligente sur Hugging Face Spaces.

## Étape 1 : Créer un espace

1. Allez sur [huggingface.co/new-space](https://huggingface.co/new-space)
2. Remplissez :
   - **Owner** : votre utilisateur ou une organisation
   - **Space name** : `data-viz-intelligent` (ou autre)
   - **License** : MIT
   - **SDK** : **Streamlit**
   - **Space hardware** : CPU basic (gratuit)
3. Cliquez sur **Create Space**

## Étape 2 : Pousser le code

### Option A : Via Git (recommandé)

```bash
cd c:\Users\user\Downloads\projetFINAL

# Si pas encore un dépôt Git :
git init
git add app.py requirements.txt README.md LICENSE src/ DEPLOI_HUGGINGFACE.md
git commit -m "Deploy to HF Spaces"

# Ajouter le remote Hugging Face (remplacez USER et SPACE_NAME)
# Créez d'abord le Space sur HF, puis récupérez l'URL
git remote add hf https://huggingface.co/spaces/USER/SPACE_NAME

# Pousser (HF utilise souvent "main" ou "master")
git push hf main
# ou si votre branche s'appelle master : git push hf master
```

### Option B : Upload manuel

1. Dans votre Space HF, allez dans **Files**
2. Cliquez sur **Add file** → **Upload files**
3. Envoyez tous les fichiers nécessaires :
   - `app.py` (racine)
   - `requirements.txt`
   - `README.md`
   - `src/data_viz_app/` (tout le dossier)
   - `LICENSE`

### Fichiers à NE PAS envoyer

- `.env` (contient la clé API, jamais la commiter)
- `__pycache__/`
- `.pytest_cache/`
- `poetry.lock` (optionnel, requirements.txt suffit)
- `Titanic-Dataset.csv`, `Housing.csv` (optionnel, l'app charge les données autrement)

## Étape 3 : Configurer la clé API Gemini

1. Dans votre Space, cliquez sur **Settings** (engrenage)
2. Allez dans **Repository secrets**
3. Cliquez sur **New secret**
4. Nom : `GEMINI_API_KEY`
5. Valeur : votre clé Gemini (https://aistudio.google.com/app/apikey)
6. Sauvegardez

Les secrets sont injectés comme variables d'environnement. L'application les utilisera automatiquement.

## Étape 4 : Lancer le Space

1. Une fois les fichiers poussés, HF démarre automatiquement le build
2. Allez dans l'onglet **App** pour voir l'application
3. Le premier démarrage peut prendre 1–2 minutes (installation des dépendances)

## Structure attendue sur HF Spaces

```
data-viz-intelligent/
├── app.py              ← Point d'entrée Streamlit
├── requirements.txt
├── README.md           ← Contient le YAML sdk: streamlit
├── LICENSE
└── src/
    └── data_viz_app/
        ├── __init__.py
        ├── app.py
        ├── data_loader.py
        ├── llm_client.py
        └── visualizations.py
```

## Dépannage

### L'app ne démarre pas
- Vérifiez les logs dans l'onglet **Logs**
- Vérifiez que `requirements.txt` contient toutes les dépendances

### Erreur "GEMINI_API_KEY non définie"
- Vérifiez que le secret `GEMINI_API_KEY` est bien défini dans Settings → Repository secrets
- Redémarrez le Space (Settings → Factory reboot)

### Erreur kaleido / export PNG
- `kaleido>=1.0` est dans requirements.txt ; le build HF l'installe
- Si l'erreur persiste, un redémarrage du Space peut aider

## Lien vers l'app

Après déploiement, votre app sera accessible à :
`https://huggingface.co/spaces/VOTRE_USER/data-viz-intelligent`
