"""Point d'entrée Streamlit - Lancer avec: streamlit run app.py"""

import os
import sys

# Ajouter src/ au path pour exécution sans installation du package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from data_viz_app.app import main

if __name__ == "__main__":
    main()
