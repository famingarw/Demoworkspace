# Faminga WiSK Demo Project

This demo project gives WiSK-AWiGIS mentees a practical VS Code workspace for Faminga data and AI work. It is based on the local guide `VS Code for Data and AI Projects-2026050612134114 ALL.pdf` and adapts its workflow into a small agronomic intelligence prototype.

The project uses synthetic field and IoT data only. It supports Faminga's 2026 mandate to move from 7,800+ pilot farmers toward 10,000 active users, protect verified impact performance, and build disciplined Week 3 baseline artifacts for GeoAI, GIS/VRA, and dashboard workstreams.

## What Mentees Will Practice

- Open a complete project folder in VS Code.
- Create and select a Python virtual environment.
- Install data and AI project dependencies from `requirements.txt`.
- Use Ruff formatting and linting from VS Code.
- Run Python scripts from the integrated terminal.
- Run a Jupyter notebook from VS Code.
- Launch a small Streamlit dashboard.
- Commit clean work with Git after each milestone.

## Project Structure

```text
demo project/
  .vscode/                 VS Code workspace settings and extension recommendations
  dashboard/               Streamlit dashboard prototype
  data/                    Synthetic Faminga field and sensor dataset
  docs/                    Data dictionary and mentee tasks
  notebooks/               Guided VS Code/Jupyter notebook
  scripts/                 Terminal entry points
  src/faminga_wiski_demo/  Reusable Python logic
  tests/                   Unit tests for recommendation rules
```

## Strategic Mandate

This demo is not an academic exercise. It trains mentees to convert soil, crop, and field data into decision-grade recommendations that support ecological intensification:

- Higher farmer productivity without expanding land footprints.
- Better irrigation discipline toward Faminga's validated water-use reduction potential.
- More precise soil interventions for yield protection.
- Practical dashboards that can later support user activation, field follow-up, and the USD 309,816 revenue target.

## Setup in VS Code

1. Open VS Code.
2. Choose `File > Open Folder`.
3. Select this folder: `D:\dev\famingaltd\wiski\demo project`.
4. Open the Command Palette with `Ctrl+Shift+P`.
5. Run `Python: Create Environment`.
6. Choose `Venv`, select your Python version, and use `requirements.txt` when VS Code asks for dependencies.
7. Run `Python: Select Interpreter` and select the new environment.

Terminal alternative:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Demo

Run the command-line prototype:

```powershell
python scripts\run_demo.py
```

Run the tests:

```powershell
python -m pytest
```

Run the dashboard:

```powershell
streamlit run dashboard\app.py
```

Open the notebook:

```text
notebooks/01_faminga_wiski_demo.ipynb
```

Select the same `.venv` kernel before running notebook cells.

## Expected Learning Output

By the end, each mentee should be able to explain:

- Which fields are high priority for intervention and why.
- How moisture, pH, NPK, disease pressure, and post-harvest risk affect recommendations.
- Which recommendation can be translated into a low-literacy farmer message.
- How the same rules could evolve into a SQL-fed dashboard or mobile app feature.

## Executive Accountability

- Cynthia Anguza: extend the risk score into a baseline yield or disease-risk notebook.
- Elizabeth Nyaguthi Githui: convert the synthetic field records into mapped boundaries and sensor overlays.
- Lucy Chepkemoi Ruto: strengthen the dashboard into a management-ready operational view.
- Uwase Hadidja, Data Science: validate the data schema for future SQL-fed dashboards.

The soil does not lie, and neither do our numbers. Treat every notebook, chart, and recommendation as a step toward investable field intelligence.
