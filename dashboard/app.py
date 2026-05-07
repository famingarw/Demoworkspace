from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from faminga_wiski_demo.soil_rules import recommendation_for_field, summarize_fields  # noqa: E402


st.set_page_config(page_title="Faminga WiSK Demo", layout="wide")

st.title("Faminga WiSK Agronomic Intelligence Demo")
st.caption("Synthetic field data for VS Code, Jupyter, dashboard, and Git practice.")

data_path = PROJECT_ROOT / "data" / "synthetic_faminga_fields.csv"
df = pd.read_csv(data_path)
rows = df.to_dict(orient="records")
recommendations = [recommendation_for_field(row) for row in rows]
recommendation_df = pd.DataFrame([item.__dict__ for item in recommendations])
summary = summarize_fields(rows)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Fields", summary["field_count"])
col2.metric("Average moisture", f"{summary['average_moisture_pct']}%")
col3.metric("Average NDVI", summary["average_ndvi"])
col4.metric("High priority", f"{summary['high_priority_count']} fields")

left, right = st.columns([1.1, 1])

with left:
    st.subheader("Risk by Field")
    risk_chart = px.bar(
        recommendation_df.sort_values("risk_score", ascending=False),
        x="field_id",
        y="risk_score",
        color="priority",
        hover_data=["district", "crop", "action"],
        color_discrete_map={"High": "#b91c1c", "Medium": "#b45309", "Low": "#15803d"},
    )
    risk_chart.update_layout(yaxis_title="Risk score", xaxis_title="Field ID")
    st.plotly_chart(risk_chart, use_container_width=True)

with right:
    st.subheader("Moisture vs Disease Pressure")
    scatter = px.scatter(
        df,
        x="soil_moisture_pct",
        y="disease_pressure_pct",
        size="area_ha",
        color="crop",
        hover_data=["field_id", "district", "ndvi"],
    )
    scatter.update_layout(xaxis_title="Soil moisture (%)", yaxis_title="Disease pressure (%)")
    st.plotly_chart(scatter, use_container_width=True)

st.subheader("Farmer-Facing Recommendations")
st.dataframe(
    recommendation_df[
        ["field_id", "district", "crop", "priority", "risk_score", "action", "farmer_message"]
    ],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Mentee Review Prompts")
st.markdown(
    """
- Cynthia: Which variables should be added before this becomes a credible baseline yield-risk model?
- Elizabeth: Which fields need boundary validation before sensor overlay and VRA classification?
- Lucy: Which operational metric should be added first for a management dashboard?
"""
)
