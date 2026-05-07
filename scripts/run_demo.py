from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from faminga_wiski_demo.soil_rules import (  # noqa: E402
    load_field_rows,
    recommendation_for_field,
    summarize_fields,
    write_recommendations,
)


def main() -> None:
    data_path = PROJECT_ROOT / "data" / "synthetic_faminga_fields.csv"
    output_path = PROJECT_ROOT / "outputs" / "field_recommendations.csv"

    rows = load_field_rows(data_path)
    summary = summarize_fields(rows)
    recommendations = [recommendation_for_field(row) for row in rows]
    write_recommendations(rows, output_path)

    print("Faminga WiSK Demo Project")
    print("=========================")
    print(f"Fields analyzed: {summary['field_count']}")
    print(f"Average soil moisture: {summary['average_moisture_pct']}%")
    print(f"Average NDVI: {summary['average_ndvi']}")
    print(f"High-priority fields: {summary['high_priority_count']} ({summary['high_priority_share_pct']}%)")
    print()
    print("Top field recommendations:")

    for item in sorted(recommendations, key=lambda rec: rec.risk_score, reverse=True)[:5]:
        print(f"- {item.field_id} | {item.priority} | score {item.risk_score}: {item.action}")

    print()
    print(f"Recommendation file written to: {output_path}")


if __name__ == "__main__":
    main()
