"""Tests pour le module de chargement de données."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from data_viz_app.data_loader import get_column_summary, load_csv


def test_load_csv():
    """Test chargement CSV."""
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        df.to_csv(f.name, index=False)
        result = load_csv(f.name)
    assert len(result) == 2
    assert list(result.columns) == ["a", "b"]


def test_load_csv_not_found():
    """Test fichier non trouvé."""
    with pytest.raises(FileNotFoundError, match="non trouvé"):
        load_csv("/chemin/inexistant.csv")


def test_get_column_summary():
    """Test résumé des colonnes."""
    df = pd.DataFrame({
        "genre": ["pop", "rock"],
        "popularity": [80, 70],
    })
    summary = get_column_summary(df)
    assert "genre" in summary
    assert "popularity" in summary
