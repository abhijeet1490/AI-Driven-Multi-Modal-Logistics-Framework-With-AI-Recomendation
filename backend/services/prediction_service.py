from dataclasses import dataclass
from typing import Any
import numpy as np

@dataclass
class PredictionResult:
    cost: float
    time: float
    co2: float

def make_mock_prediction(
    distance_km: float, weight_kg: float, traffic_level: float, transport_mode: str
) -> PredictionResult:
    """
    Simple deterministic formulas used when the ML model is not available.
    These are intentionally straightforward and transparent.
    """
    # Adjust mock logic based on transport mode
    base_cost_per_km = 1.4
    cost_per_kg = 0.04
    base_speed_kmph = 65.0
    co2_per_km = 0.16
    co2_per_kg = 0.00035

    if transport_mode == 'rail':
        base_cost_per_km = 0.8
        base_speed_kmph = 50.0  # Steady but slower
        co2_per_km = 0.08       # More eco-friendly
        traffic_level = 1       # Rails largely unaffected by highway traffic
    elif transport_mode == 'air':
        base_cost_per_km = 5.0
        cost_per_kg = 0.50
        base_speed_kmph = 500.0 # Very fast
        co2_per_km = 0.8        # High emissions
        traffic_level = 1       # Air largely unaffected by highway traffic
    # Default is truck (original values)

    traffic_surcharge = 6.0
    cost = (
        distance_km * base_cost_per_km
        + weight_kg * cost_per_kg
        + traffic_level * traffic_surcharge
    )

    traffic_penalty = 2.5
    effective_speed = max(20.0, base_speed_kmph - traffic_penalty * traffic_level)
    time_hours = distance_km / effective_speed

    co2_traffic_factor = 1.2
    co2_kg = (
        distance_km * co2_per_km
        + weight_kg * co2_per_kg
        + traffic_level * co2_traffic_factor
    )

    return PredictionResult(cost=cost, time=time_hours, co2=co2_kg)

def make_model_prediction(
    model: Any, distance_km: float, weight_kg: float, traffic_level: float, transport_mode: str
) -> PredictionResult:
    """
    Use the trained model to make a prediction. 
    (Note: The original model was trained only on distance/weight/traffic. 
    We scale the outputs similarly to mock mode for the demonstration prototype).
    """
    features = np.array([[distance_km, weight_kg, traffic_level]], dtype=float)
    cost, time_hours, co2_kg = model.predict(features)[0]

    cost_multiplier = 1.0
    time_multiplier = 1.0
    co2_multiplier = 1.0

    if transport_mode == 'rail':
        cost_multiplier = 0.7
        time_multiplier = 1.2
        co2_multiplier = 0.5
    elif transport_mode == 'air':
        cost_multiplier = 2.5
        time_multiplier = 0.4
        co2_multiplier = 1.3

    cost *= cost_multiplier
    time_hours *= time_multiplier
    co2_kg *= co2_multiplier

    return PredictionResult(cost=float(cost), time=float(time_hours), co2=float(co2_kg))
