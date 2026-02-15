# Note – 3 exemples de problématiques / datasets et résultats

Rendu du projet Data Visualization Intelligente – Master 2 BDIA.

---

## Exemple 1 : Prix des logements

### Problématique
**Quels facteurs influencent le prix des logements ?**

### Dataset
- **Source** : `Housing.csv` (fichier CSV)
- **Colonnes** : price, area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking, prefarea, furnishingstatus
- **Taille** : ~545 lignes

### Résultats de l'application

L'application génère 3 propositions de visualisation. Exemples typiques :

| Proposition | Type | Colonnes | Justification |
|-------------|------|----------|---------------|
| 1 | **Bar** | Prix moyen par furnishingstatus | Compare le prix selon le niveau d'aménagement (furnished, semi-furnished, unfurnished). Permet d'identifier l'impact du mobilier sur le prix. |
| 2 | **Scatter** | area (X) vs price (Y) | Montre la corrélation entre superficie et prix. Bon data-ink ratio pour visualiser la relation linéaire. |
| 3 | **Box** | Prix par nombre de chambres (bedrooms) | Affiche la distribution des prix par catégorie. Permet de voir la dispersion et les outliers pour chaque type de logement. |

### Visualisation retenue
Par exemple : **Graphique à barres – Prix moyen par niveau d'aménagement**, qui montre que les logements « furnished » ont en moyenne un prix plus élevé que « unfurnished ».

---

## Exemple 2 : Survie des passagers du Titanic

### Problématique
**Quels profils de passagers avaient le plus de chances de survie ?**

### Dataset
- **Source** : `Titanic-Dataset.csv` (fichier CSV)
- **Colonnes** : PassengerId, Survived, Pclass, Sex, Age, SibSp, Parch, Fare, Embarked
- **Taille** : ~891 passagers

### Résultats de l'application

| Proposition | Type | Colonnes | Justification |
|-------------|------|----------|---------------|
| 1 | **Bar** | Taux de survie par Pclass (1ère, 2e, 3e classe) | Compare les proportions de survivants par classe. La 1ère classe a nettement plus de survivants. |
| 2 | **Bar** | Taux de survie par Sex | Montre l’effet « femmes et enfants d’abord » : les femmes ont un taux de survie bien plus élevé. |
| 3 | **Box** | Fare (prix du billet) par Survived | Distribution du tarif payé selon la survie. Les survivants ont en moyenne payé plus cher (corrélation avec la classe). |

### Visualisation retenue
Par exemple : **Graphique à barres – Taux de survie par classe**, qui illustre que les passagers de 1ère classe avaient les meilleures chances de survie, suivis de la 2e puis de la 3e classe.

---

## Exemple 3 : Style de musique et ventes (Spotify)

### Problématique
**Quel style de musique maximise le nombre de ventes pour une entreprise de production musicale ?**

### Dataset
- **Source** : `maharshipandya/spotify-tracks-dataset` (Hugging Face)
- **Colonnes** : track_id, artists, track_name, popularity, duration_ms, track_genre, danceability, energy, valence, tempo, etc.
- **Taille** : 114 000 pistes, 125 genres

### Résultats de l'application

| Proposition | Type | Colonnes | Justification |
|-------------|------|----------|---------------|
| 1 | **Bar** | Popularité moyenne par track_genre (top 10 ou 15) | La popularité est un proxy des ventes/streams. Permet d’identifier les genres les plus rentables. |
| 2 | **Box** | Distribution de la popularité par genre (top 10) | Montre la variabilité : certains genres ont une popularité stable, d’autres plus dispersée (risque). |
| 3 | **Bar** | Nombre de pistes par genre | Visualise le volume de contenu par genre : saturation du marché vs opportunités. |

### Visualisation retenue
Par exemple : **Graphique à barres – Popularité moyenne par genre musical**, qui met en évidence les genres (pop, hip-hop, dance, etc.) avec la popularité moyenne la plus élevée, utiles pour orienter la production.

---

## Synthèse

L'application a correctement :
- Analysé chaque problématique et la structure des datasets ;
- Proposé 3 visualisations adaptées et justifiées ;
- Respecté les bonnes pratiques (choix de graphique, lisibilité, data-ink ratio).

Les visualisations sont générées automatiquement par le LLM (Gemini) et peuvent être exportées en PNG.
