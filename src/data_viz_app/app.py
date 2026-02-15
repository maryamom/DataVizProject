"""Application Streamlit - Data Visualization Intelligente."""

import html
import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from .data_loader import get_column_summary, load_data
from .llm_client import analyze_and_propose_visualizations, get_client
from .visualizations import create_chart, figure_to_png_bytes

# Configuration de la page
st.set_page_config(
    page_title="Data Visualization Intelligente",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style personnalisé
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); }
    h1 { color: #0f172a; font-weight: 700; letter-spacing: -0.02em; }
    h2, h3 { color: #1e293b; font-weight: 600; }

    .proposal-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.08), 0 2px 4px -2px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    .proposal-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.08);
        border-color: #94a3b8;
    }
    .proposal-card-1 { border-left: 4px solid #3b82f6; }
    .proposal-card-2 { border-left: 4px solid #06b6d4; }
    .proposal-card-3 { border-left: 4px solid #8b5cf6; }

    .proposal-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    .proposal-type {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.85rem;
        color: #64748b;
        background: #f1f5f9;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        margin-bottom: 0.75rem;
    }
    .proposal-justification {
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.5;
        padding: 0.75rem;
        background: #f8fafc;
        border-radius: 8px;
        border-left: 3px solid #cbd5e1;
    }

    .proposals-header {
        margin-bottom: 1.5rem;
    }
    .proposals-header h3 {
        margin: 0;
        font-size: 1.35rem;
    }
    .proposals-subtitle {
        color: #64748b;
        font-size: 0.95rem;
        margin-top: 0.25rem;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="column"] {
        padding: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


def main() -> None:
    st.title("📊 Data Visualization Intelligente")
    st.markdown(
        "*Application pilotée par LLM pour générer automatiquement des visualisations "
        "adaptées à votre problématique métier.*"
    )

    # Sidebar - Configuration
    with st.sidebar:
        st.header("Configuration")
        dataset_source = st.radio(
            "Source des données",
            ["CSV (fichier)", "Hugging Face"],
            index=1,
        )

        df: pd.DataFrame | None = None

        if dataset_source == "CSV (fichier)":
            uploaded = st.file_uploader("Choisir un fichier CSV", type=["csv"])
            if uploaded:
                df = pd.read_csv(uploaded)
                st.session_state["dataset_df"] = df
            else:
                df = st.session_state.get("dataset_df")
        else:
            dataset_id = st.text_input(
                "ID du dataset Hugging Face",
                value="maharshipandya/spotify-tracks-dataset",
                help="Ex: maharshipandya/spotify-tracks-dataset",
            )
            if dataset_id and st.button("Charger le dataset"):
                with st.spinner("Chargement..."):
                    try:
                        df = load_data(source="huggingface", dataset_id=dataset_id)
                        st.session_state["dataset_df"] = df
                        st.success(f"Chargé : {len(df)} lignes, {len(df.columns)} colonnes")
                    except Exception as e:
                        st.error(str(e))
            df = st.session_state.get("dataset_df")

    # Zone principale
    problem = st.text_area(
        "Problématique",
        value="Quel style de musique maximise le nombre de ventes pour une entreprise de production musicale ?",
        height=80,
        help="Décrivez la question métier à laquelle vous voulez répondre.",
    )

    if df is None and dataset_source == "CSV (fichier)":
        st.info("👈 Uploadez un fichier CSV ou chargez un dataset Hugging Face dans la barre latérale.")
        return

    if df is None:
        st.warning("Chargez un dataset pour continuer.")
        return

    # Aperçu des données
    with st.expander("Aperçu des données"):
        st.dataframe(df.head(20), use_container_width=True)

    # Bouton pour générer les propositions
    if st.button("🚀 Générer les propositions de visualisation", type="primary"):
        if not os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
            st.error(
                "**GEMINI_API_KEY** n'est pas définie. "
                "Définissez-la dans un fichier `.env` ou dans les variables d'environnement. "
                "Clé gratuite sur https://aistudio.google.com/app/apikey"
            )
            st.code("export GEMINI_API_KEY=votre_clé", language="bash")
            return

        with st.spinner("Analyse de la problématique et génération des propositions..."):
            try:
                column_summary = get_column_summary(df)
                sample_data = df.head(5).to_string()

                client = get_client()
                result = analyze_and_propose_visualizations(
                    problem=problem,
                    column_summary=column_summary,
                    sample_data=sample_data,
                    client=client,
                )
                proposals = result.get("proposals", [])
                st.session_state["proposals"] = proposals
                st.session_state["df"] = df
            except Exception as e:
                st.error(f"Erreur lors de l'appel au LLM : {e}")
                raise

    # Affichage des 3 propositions
    if "proposals" in st.session_state:
        proposals = st.session_state["proposals"]
        df = st.session_state["df"]

        # Icônes par type de graphique
        CHART_ICONS = {
            "bar": "📊",
            "line": "📈",
            "scatter": "⬤",
            "pie": "🥧",
            "histogram": "📉",
            "box": "📦",
        }

        st.markdown('<div class="proposals-header"><h3>✨ Choisissez une visualisation</h3><p class="proposals-subtitle">Sélectionnez la proposition qui vous convient le mieux</p></div>', unsafe_allow_html=True)

        cols = st.columns(3)
        for i, prop in enumerate(proposals):
            chart_type_raw = prop.get("chart_type", "bar")
            chart_type = chart_type_raw.lower()
            icon = CHART_ICONS.get(chart_type, "📊")
            title = html.escape(prop.get("title", "Sans titre"))
            justification = html.escape(prop.get("justification", ""))

            with cols[i]:
                st.markdown(
                    f'<div class="proposal-card proposal-card-{i + 1}">'
                    f'<div class="proposal-title">Proposition {i + 1} — {title}</div>'
                    f'<div class="proposal-type">{icon} {chart_type_raw}</div>'
                    f'<div class="proposal-justification">{justification}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"✓ Choisir cette visualisation",
                    key=f"sel_{i}",
                    use_container_width=True,
                ):
                    st.session_state["selected_proposal"] = prop
                    st.session_state["selected_index"] = i
                    st.rerun()

        # Visualisation finale
        if "selected_proposal" in st.session_state:
            selected = st.session_state["selected_proposal"]
            st.divider()
            st.subheader("📈 Visualisation finale")

            try:
                fig = create_chart(
                    df,
                    selected,
                    title=selected.get("title", "Visualisation"),
                )
                st.plotly_chart(fig, use_container_width=True)

                # Export PNG
                png_bytes = figure_to_png_bytes(fig)
                st.download_button(
                    label="📥 Télécharger en PNG",
                    data=png_bytes,
                    file_name="visualisation.png",
                    mime="image/png",
                    key="download_png",
                )
            except Exception as e:
                st.error(f"Erreur lors de la génération du graphique : {e}")
                st.code(str(e))


if __name__ == "__main__":
    main()
