from flask import Blueprint, jsonify, request, current_app
from typing import Any, Dict
from services.prediction_service import make_model_prediction, make_mock_prediction

prediction_bp = Blueprint("prediction_bp", __name__)

@prediction_bp.route("/health", methods=["GET"])
def health() -> Any:
    mock_mode = current_app.config.get("MOCK_MODE", True)
    return jsonify(
        {
            "status": "ok",
            "mock_mode": mock_mode,
        }
    )

@prediction_bp.route("/predict_route", methods=["POST"])
def predict_route() -> Any:
    model = current_app.config.get("MODEL")
    mock_mode = current_app.config.get("MOCK_MODE", True)

    try:
        # Accept both application/json and text/json
        payload: Dict[str, Any] = request.get_json(force=True, silent=False)
    except Exception:
        return (
            jsonify({"success": False, "error": "Invalid JSON payload."}),
            400,
        )

    missing_fields = [
        field
        for field in ("distance", "weight", "traffic")
        if field not in payload
    ]
    if missing_fields:
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Missing fields: {', '.join(missing_fields)}",
                }
            ),
            400,
        )

    transport_mode = payload.get("transport_mode", "truck")
    valid_modes = ["truck", "rail", "three_wheeler"]
    if transport_mode not in valid_modes:
         return (
             jsonify(
                 {
                     "success": False,
                     "error": f"Invalid transport_mode. Must be one of: {', '.join(valid_modes)}",
                 }
             ),
             400,
         )

    try:
        distance_km = float(payload["distance"])
        weight_kg = float(payload["weight"])
        traffic_level = float(payload["traffic"])
        road_quality = int(payload.get("road_quality", 1))
    except (TypeError, ValueError):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "distance, weight, traffic, and road_quality must be numeric.",
                }
            ),
            400,
        )

    if distance_km <= 0 or weight_kg <= 0:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "distance and weight must be positive.",
                }
            ),
            400,
        )

    if traffic_level < 1 or traffic_level > 10:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "traffic must be between 1 and 10.",
                }
            ),
            400,
        )

    try:
        if not mock_mode and model is not None:
            result = make_model_prediction(
                model, distance_km, weight_kg, traffic_level, transport_mode, road_quality
            )
        else:
            result = make_mock_prediction(distance_km, weight_kg, traffic_level, transport_mode, road_quality)
    except Exception as exc:
        print(f"[ERROR] Prediction failed with model: {exc}. Falling back to MOCK.")
        current_app.config["MOCK_MODE"] = True
        mock_mode = True
        result = make_mock_prediction(distance_km, weight_kg, traffic_level, transport_mode, road_quality)

    response = {
        "success": True,
        "transport_mode": transport_mode,
        "data": {
            "cost": result.cost,
            "time": result.time,
            "co2": result.co2,
        },
        "mock_mode": mock_mode,
    }
    return jsonify(response)
