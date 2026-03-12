import os
import pickle
from typing import Any, Optional, Tuple

def get_model_path() -> str:
    """Return the absolute path to the logistics model."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "models", "logistics_model.pkl")

def load_model() -> Tuple[Optional[Any], bool]:
    """
    Attempt to load the trained model from disk.

    Returns:
        (model, mock_mode)
        - model: the loaded model instance or None
        - mock_mode: True if we should fall back to mock predictions
    """
    path = get_model_path()
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
        print(f"[INFO] Loaded model from '{path}'.")
        return model, False
    except FileNotFoundError:
        print(f"[WARN] Model file '{path}' not found. Starting in MOCK_MODE.")
    except Exception as exc:
        print(f"[ERROR] Failed to load model from '{path}': {exc}")

    return None, True
