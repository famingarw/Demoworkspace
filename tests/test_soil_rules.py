from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from faminga_wiski_demo.soil_rules import (
    calculate_risk_score,
    classify_intervention_priority,
    load_field_rows,
    recommendation_for_field,
    summarize_fields,
)


DATA_PATH = PROJECT_ROOT / "data" / "synthetic_faminga_fields.csv"


class SoilRulesTest(unittest.TestCase):
    def test_load_field_rows_coerces_numbers(self):
        rows = load_field_rows(DATA_PATH)

        self.assertEqual(len(rows), 12)
        self.assertIsInstance(rows[0]["soil_moisture_pct"], float)

    def test_high_risk_field_gets_high_priority(self):
        row = {
            "field_id": "TEST-001",
            "farmer_group": "Demo Group",
            "district": "Kayonza",
            "crop": "maize",
            "soil_moisture_pct": 15,
            "soil_ph": 5.1,
            "nitrogen_ppm": 20,
            "phosphorus_ppm": 8,
            "potassium_ppm": 90,
            "ndvi": 0.42,
            "disease_pressure_pct": 44,
            "post_harvest_risk_pct": 36,
            "last_visit_days": 24,
            "market_access_km": 18,
        }

        score = calculate_risk_score(row)
        recommendation = recommendation_for_field(row)

        self.assertGreaterEqual(score, 65)
        self.assertEqual(recommendation.priority, "High")
        self.assertIn("water attention", recommendation.farmer_message)

    def test_priority_boundaries(self):
        self.assertEqual(classify_intervention_priority(20), "Low")
        self.assertEqual(classify_intervention_priority(35), "Medium")
        self.assertEqual(classify_intervention_priority(65), "High")

    def test_summary_reports_high_priority_share(self):
        rows = load_field_rows(DATA_PATH)
        summary = summarize_fields(rows)

        self.assertEqual(summary["field_count"], 12)
        self.assertGreaterEqual(summary["high_priority_share_pct"], 0)
        self.assertLessEqual(summary["high_priority_share_pct"], 100)


if __name__ == "__main__":
    unittest.main()
