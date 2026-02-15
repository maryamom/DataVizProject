"""Tests pour le module de visualisation."""

import pytest
import pandas as pd

from data_viz_app.visualizations import create_chart, _prepare_data


def test_prepare_data_simple():
    """Test de la préparation des données sans groupement."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
    result = _prepare_data(df, "a", "b", None, "mean")
    assert len(result) == 3
    assert list(result.columns) == ["a", "b"]


def test_prepare_data_with_group():
    """Test de la préparation avec groupement."""
    df = pd.DataFrame({
        "genre": ["pop", "pop", "rock", "rock"],
        "popularity": [80, 90, 70, 60],
    })
    result = _prepare_data(df, "genre", "popularity", None, "mean")
    assert len(result) == 2
    assert result["popularity"].tolist() == [85.0, 65.0]


def test_create_chart_bar():
    """Test création d'un graphique bar."""
    df = pd.DataFrame({
        "genre": ["pop", "rock", "jazz"],
        "popularity": [85, 65, 55],
    })
    config = {
        "chart_type": "bar",
        "x_column": "genre",
        "y_column": "popularity",
        "group_by": None,
        "aggregation": "none",
    }
    fig = create_chart(df, config, title="Test")
    assert fig is not None
    assert fig.layout.title.text == "Test"


def test_create_chart_invalid_column():
    """Test avec une colonne invalide."""
    df = pd.DataFrame({"a": [1, 2], "b": [10, 20]})
    config = {
        "chart_type": "bar",
        "x_column": "inexistant",
        "y_column": "b",
        "group_by": None,
        "aggregation": "none",
    }
    with pytest.raises(ValueError, match="inexistant"):
        create_chart(df, config, "Test")
