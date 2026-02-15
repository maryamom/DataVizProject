"""Client LLM pour l'analyse et la génération des propositions de visualisation."""

import json
import os
from typing import Any

from google import genai
from google.genai import types


# Bonnes pratiques de visualisation (référence cours)
VISUALIZATION_BEST_PRACTICES = """
Bonnes pratiques de visualisation (Edward Tufte, Stephen Few) :
- Data-ink ratio maximal : maximiser l'encre utilisée pour les données vs décoration
- Chartjunk : éviter les éléments décoratifs superflus (3D inutile, dégradés excessifs)
- Choix du type de graphique selon les données :
  - Comparaisons : barres, colonnes
  - Évolution temporelle : lignes
  - Répartition/proportions : camembert (peu de catégories), barres empilées
  - Corrélations : scatter plot
  - Distributions : histogramme, box plot
- Lisibilité : titres clairs, axes étiquetés, légendes explicites
- Couleurs : palette cohérente, accessibilité (daltonisme), contraste suffisant
"""


def get_client() -> genai.Client:
    """Retourne un client Gemini configuré."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY non définie. Définissez-la dans .env ou les variables d'environnement."
        )
    return genai.Client(api_key=api_key)


def build_system_prompt() -> str:
    """Construit le prompt système pour le raisonnement structuré."""
    return f"""Tu es un expert en data visualization et en analyse de données.
{VISUALIZATION_BEST_PRACTICES}

Tu dois analyser une problématique métier et un dataset, puis proposer 3 visualisations différentes.
Chaque proposition doit :
1. Être adaptée à la problématique
2. Respecter les bonnes pratiques ci-dessus
3. Utiliser les colonnes disponibles dans le dataset
4. Être justifiée (pourquoi ce type de graphique, quelles colonnes, quel message)

Format de réponse strictement JSON :
{{
  "proposals": [
    {{
      "title": "Titre du graphique",
      "chart_type": "bar|line|scatter|pie|histogram|box",
      "x_column": "nom_colonne",
      "y_column": "nom_colonne",
      "group_by": "nom_colonne ou null",
      "aggregation": "sum|mean|count|none",
      "justification": "Explication détaillée de 2-3 phrases"
    }},
    ...
  ]
}}

Réponds UNIQUEMENT avec le JSON valide, sans texte avant ou après."""


def analyze_and_propose_visualizations(
    problem: str,
    column_summary: str,
    sample_data: str,
    client: genai.Client | None = None,
) -> dict[str, Any]:
    """
    Analyse la problématique et propose 3 visualisations via LLM (scaffolding).
    """
    if client is None:
        client = get_client()

    user_message = f"""Problématique : {problem}

Résumé des colonnes du dataset :
{column_summary}

Aperçu des données (5 premières lignes) :
{sample_data}

Propose 3 visualisations différentes, chacune adaptée à la problématique et aux données disponibles.
Réponds en JSON uniquement."""

    model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    response = client.models.generate_content(
        model=model,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=build_system_prompt(),
            temperature=0.3,
        ),
    )

    content = (response.text or "").strip()
    # Nettoyer d'éventuels blocs markdown
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()

    return json.loads(content)
