"""
app.py

Flask backend for the "AI-Powered Multi-Modal Transport System".
"""

import os
import sys

# Ensure backend directory is in the Python path to allow running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from utils.model_loader import load_model
from routes.prediction_routes import prediction_bp

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  # enable CORS for all routes

    model, mock_mode = load_model()
    
    # Store ML model and mock status in the app config
    app.config["MODEL"] = model
    app.config["MOCK_MODE"] = mock_mode

    # Register modular blueprints
    app.register_blueprint(prediction_bp)

    return app

app = create_app()

if __name__ == "__main__":
    # For local development only; in production use a proper WSGI server.
    app.run(host="0.0.0.0", port=5001, debug=True)
