# Data Dictionary

The dataset is synthetic and is safe for mentee training. It does not contain live farmer records.

| Column | Type | Description |
| --- | --- | --- |
| `field_id` | Text | Synthetic field identifier. |
| `farmer_group` | Text | Cooperative, cell, or farmer group label. |
| `district` | Text | Rwanda district used for the training scenario. |
| `crop` | Text | Crop under monitoring. |
| `area_ha` | Number | Field area in hectares. |
| `sensor_id` | Text | Synthetic IoT sensor identifier. |
| `soil_moisture_pct` | Number | Soil moisture percentage from the sensor layer. |
| `soil_ph` | Number | Soil pH reading. |
| `nitrogen_ppm` | Number | Nitrogen concentration in parts per million. |
| `phosphorus_ppm` | Number | Phosphorus concentration in parts per million. |
| `potassium_ppm` | Number | Potassium concentration in parts per million. |
| `ndvi` | Number | Vegetation index proxy from 0 to 1. |
| `disease_pressure_pct` | Number | Synthetic disease pressure estimate. |
| `post_harvest_risk_pct` | Number | Synthetic post-harvest loss risk estimate. |
| `last_visit_days` | Number | Days since a field team or agronomist follow-up. |
| `market_access_km` | Number | Approximate distance to a market channel in kilometers. |

## Governance Note

This file models the documentation discipline required before any SQL-fed dashboard, mobile-app workflow, or investor-facing metric can be trusted. Live farmer data requires explicit Faminga approval and role-based access controls.
