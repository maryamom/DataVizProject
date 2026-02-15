"""Génération des graphiques avec Plotly."""

import io
from typing import Any, Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _prepare_data(
    df: pd.DataFrame,
    x_column: str,
    y_column: str,
    group_by: Optional[str],
    aggregation: str,
) -> pd.DataFrame:
    """Prépare les données selon la configuration de la visualisation."""
    if x_column not in df.columns:
        raise ValueError(f"Colonne X '{x_column}' absente du dataset")
    if y_column not in df.columns:
        raise ValueError(f"Colonne Y '{y_column}' absente du dataset")

    if group_by and group_by not in df.columns:
        raise ValueError(f"Colonne group_by '{group_by}' absente du dataset")

    if group_by:
        agg_func = aggregation if aggregation != "none" else "first"
        if aggregation == "count":
            result = df.groupby([x_column, group_by]).size().reset_index(name=y_column or "count")
        else:
            result = (
                df.groupby([x_column, group_by])[y_column]
                .agg(agg_func)
                .reset_index()
            )
        return result

    if aggregation == "count":
        result = df.groupby(x_column).size().reset_index(name=y_column or "count")
        return result
    if aggregation != "none":
        result = df.groupby(x_column)[y_column].agg(aggregation).reset_index()
        return result

    return df[[x_column, y_column]].copy()


def create_chart(
    df: pd.DataFrame,
    config: dict[str, Any],
    title: str = "Visualisation",
) -> go.Figure:
    """
    Crée un graphique Plotly selon la configuration LLM.
    
    Args:
        df: DataFrame des données
        config: Dictionnaire avec chart_type, x_column, y_column, group_by, aggregation
        title: Titre du graphique
    """
    chart_type = config.get("chart_type", "bar").lower()
    x_column = config.get("x_column", "")
    y_column = config.get("y_column", "")
    group_by = config.get("group_by") or None
    if group_by == "null":
        group_by = None
    aggregation = config.get("aggregation", "mean")

    data = _prepare_data(df, x_column, y_column, group_by, aggregation)

    fig: go.Figure

    if chart_type == "bar":
        if group_by:
            fig = px.bar(data, x=x_column, y=y_column, color=group_by, barmode="group")
        else:
            fig = px.bar(data, x=x_column, y=y_column)
    elif chart_type == "line":
        if group_by:
            fig = px.line(data, x=x_column, y=y_column, color=group_by)
        else:
            fig = px.line(data, x=x_column, y=y_column)
    elif chart_type == "scatter":
        if group_by:
            fig = px.scatter(df, x=x_column, y=y_column, color=group_by)
        else:
            fig = px.scatter(df, x=x_column, y=y_column)
    elif chart_type == "pie":
        # Pour un pie, on agrège par catégorie (group_by ou x_column)
        dim = group_by or x_column
        if dim not in df.columns or y_column not in df.columns:
            raise ValueError(f"Colonnes {dim} ou {y_column} absentes")
        pie_data = df.groupby(dim)[y_column].sum().reset_index()
        fig = px.pie(pie_data, names=dim, values=y_column)
    elif chart_type == "histogram":
        fig = px.histogram(df, x=x_column, color=group_by if group_by else None)
    elif chart_type == "box":
        if group_by:
            fig = px.box(df, x=group_by, y=y_column)
        else:
            fig = px.box(df, y=y_column)
    else:
        # Fallback bar
        if group_by:
            fig = px.bar(data, x=x_column, y=y_column, color=group_by, barmode="group")
        else:
            fig = px.bar(data, x=x_column, y=y_column)

    # Formatage selon les bonnes pratiques
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center", font=dict(size=18)),
        xaxis_title=x_column.replace("_", " ").title(),
        yaxis_title=y_column.replace("_", " ").title(),
        legend_title=(group_by.replace("_", " ").title() if group_by else None),
        template="plotly_white",
        font=dict(size=12),
        margin=dict(t=80, b=60, l=60, r=40),
        showlegend=group_by is not None,
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    fig.update_xaxes(tickangle=-45, tickfont=dict(size=10))
    fig.update_yaxes(tickfont=dict(size=10))

    return fig


def figure_to_png_bytes(fig: go.Figure, width: int = 1200, height: int = 600) -> bytes:
    """Exporte une figure Plotly en PNG (bytes). Nécessite kaleido."""
    buf = io.BytesIO()
    try:
        fig.write_image(buf, format="png", width=width, height=height)
        buf.seek(0)
        return buf.read()
    except Exception as e:
        err_lower = str(e).lower()
        if "kaleido" in err_lower:
            msg = (
                "L'export PNG nécessite le package kaleido. "
                "Lancez dans le terminal : poetry run pip install -U kaleido\n\n"
                "Puis redémarrez l'application Streamlit (Ctrl+C puis poetry run streamlit run app.py).\n\n"
                "Si l'erreur persiste (Kaleido 1.x) : Chrome peut être requis. Essayez : "
                "poetry run python -c \"import kaleido; kaleido.get_chrome_sync()\""
            )
            raise RuntimeError(msg) from e
        raise
