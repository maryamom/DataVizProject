"""Chargement des datasets : CSV ou Hugging Face."""

from pathlib import Path
from typing import Optional

import pandas as pd

try:
    from datasets import load_dataset
    HAS_DATASETS = True
except ImportError:
    HAS_DATASETS = False


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """Charge un fichier CSV et retourne un DataFrame."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier non trouvé : {path}")
    return pd.read_csv(path)


def load_huggingface_dataset(dataset_id: str, split: str = "train") -> pd.DataFrame:
    """
    Charge un dataset Hugging Face et le convertit en DataFrame.
    Exemple : maharshipandya/spotify-tracks-dataset
    """
    if not HAS_DATASETS:
        raise ImportError(
            "La librairie 'datasets' est requise. Installez avec: pip install datasets"
        )
    ds = load_dataset(dataset_id, split=split)
    return ds.to_pandas()


def load_data(
    source: str,
    file_path: Optional[str] = None,
    dataset_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Charge les données depuis CSV ou Hugging Face.
    
    Args:
        source: "csv" ou "huggingface"
        file_path: Chemin vers le fichier CSV (si source="csv")
        dataset_id: ID du dataset Hugging Face (si source="huggingface")
    """
    if source == "csv":
        if not file_path:
            raise ValueError("file_path requis pour source='csv'")
        return load_csv(file_path)
    if source == "huggingface":
        if not dataset_id:
            raise ValueError("dataset_id requis pour source='huggingface'")
        return load_huggingface_dataset(dataset_id)
    raise ValueError(f"Source non supportée : {source}")


def get_column_summary(df: pd.DataFrame) -> str:
    """Génère un résumé des colonnes pour le contexte LLM."""
    summary = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        n_unique = df[col].nunique()
        sample = df[col].dropna().head(3).tolist()
        summary.append(f"- {col} ({dtype}): {n_unique} valeurs uniques, ex: {sample}")
    return "\n".join(summary)
