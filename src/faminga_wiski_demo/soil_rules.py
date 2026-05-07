from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class FieldRecommendation:
    field_id: str
    farmer_group: str
    district: str
    crop: str
    priority: str
    risk_score: int
    action: str
    farmer_message: str


NUMERIC_COLUMNS = {
    "area_ha",
    "soil_moisture_pct",
    "soil_ph",
    "nitrogen_ppm",
    "phosphorus_ppm",
    "potassium_ppm",
    "ndvi",
    "disease_pressure_pct",
    "post_harvest_risk_pct",
    "last_visit_days",
    "market_access_km",
}


def load_field_rows(csv_path: str | Path) -> list[dict[str, object]]:
    path = Path(csv_path)
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    return [_coerce_numeric_values(row) for row in rows]


def recommendation_for_field(row: dict[str, object]) -> FieldRecommendation:
    risk_score = calculate_risk_score(row)
    priority = classify_intervention_priority(risk_score)
    action = _select_primary_action(row)
    farmer_message = _build_farmer_message(row, action)

    return FieldRecommendation(
        field_id=str(row["field_id"]),
        farmer_group=str(row["farmer_group"]),
        district=str(row["district"]),
        crop=str(row["crop"]),
        priority=priority,
        risk_score=risk_score,
        action=action,
        farmer_message=farmer_message,
    )


def summarize_fields(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    row_list = list(rows)
    recommendations = [recommendation_for_field(row) for row in row_list]
    high_priority_count = sum(item.priority == "High" for item in recommendations)

    return {
        "field_count": len(row_list),
        "average_moisture_pct": round(mean(float(row["soil_moisture_pct"]) for row in row_list), 1),
        "average_ndvi": round(mean(float(row["ndvi"]) for row in row_list), 2),
        "high_priority_count": high_priority_count,
        "high_priority_share_pct": round(high_priority_count / len(row_list) * 100, 1),
    }


def calculate_risk_score(row: dict[str, object]) -> int:
    score = 0

    moisture = float(row["soil_moisture_pct"])
    ph = float(row["soil_ph"])
    nitrogen = float(row["nitrogen_ppm"])
    phosphorus = float(row["phosphorus_ppm"])
    potassium = float(row["potassium_ppm"])
    ndvi = float(row["ndvi"])
    disease_pressure = float(row["disease_pressure_pct"])
    post_harvest_risk = float(row["post_harvest_risk_pct"])
    last_visit_days = float(row["last_visit_days"])
    market_access_km = float(row["market_access_km"])

    if moisture < 20:
        score += 22
    elif moisture < 25:
        score += 12

    if ph < 5.5 or ph > 7.2:
        score += 14
    elif ph < 5.8:
        score += 8

    if nitrogen < 32:
        score += 14
    if phosphorus < 13:
        score += 10
    if potassium < 110:
        score += 8

    if ndvi < 0.50:
        score += 16
    elif ndvi < 0.60:
        score += 8

    if disease_pressure >= 35:
        score += 18
    elif disease_pressure >= 25:
        score += 10

    if post_harvest_risk >= 30:
        score += 12
    elif post_harvest_risk >= 22:
        score += 7

    if last_visit_days > 18:
        score += 8

    if market_access_km > 15:
        score += 4

    return min(score, 100)


def classify_intervention_priority(risk_score: int) -> str:
    if risk_score >= 65:
        return "High"
    if risk_score >= 35:
        return "Medium"
    return "Low"


def write_recommendations(rows: Iterable[dict[str, object]], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    recommendations = [recommendation_for_field(row) for row in rows]

    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "field_id",
                "farmer_group",
                "district",
                "crop",
                "priority",
                "risk_score",
                "action",
                "farmer_message",
            ],
        )
        writer.writeheader()
        for item in recommendations:
            writer.writerow(item.__dict__)

    return path


def _coerce_numeric_values(row: dict[str, str]) -> dict[str, object]:
    typed_row: dict[str, object] = {}
    for key, value in row.items():
        typed_row[key] = float(value) if key in NUMERIC_COLUMNS else value
    return typed_row


def _select_primary_action(row: dict[str, object]) -> str:
    if float(row["soil_moisture_pct"]) < 20:
        return "Prioritize irrigation scheduling and moisture follow-up."
    if float(row["nitrogen_ppm"]) < 32 or float(row["phosphorus_ppm"]) < 13:
        return "Review fertilizer plan for site-specific nutrient correction."
    if float(row["disease_pressure_pct"]) >= 35:
        return "Escalate disease scouting and crop protection advisory."
    if float(row["post_harvest_risk_pct"]) >= 30:
        return "Prepare harvest handling and market timing support."
    return "Maintain routine monitoring and reinforce good agronomic practice."


def _build_farmer_message(row: dict[str, object], action: str) -> str:
    crop = str(row["crop"])
    field_id = str(row["field_id"])

    if "irrigation" in action:
        return f"{field_id}: Your {crop} field needs water attention this week. Check moisture before applying fertilizer."
    if "fertilizer" in action:
        return f"{field_id}: Your {crop} field needs a soil nutrient review before the next input application."
    if "disease" in action:
        return f"{field_id}: Scout the {crop} field for disease signs and report photos through the Faminga app."
    if "harvest" in action:
        return f"{field_id}: Prepare harvest handling early to reduce crop loss and improve market readiness."
    return f"{field_id}: Keep monitoring your {crop} field. Current readings show no urgent intervention."
