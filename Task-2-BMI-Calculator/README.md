# BMI Calculator – OASIS Infobyte Python Internship

## Project Overview

This repository contains the completed **BMI Calculator** application developed for the **OASIS Infobyte Python Internship **. The project progresses through three phases:

* **Phase 1 – Beginner Tier** – Command‑line BMI calculator.
* **Phase 2 – Advanced Tier** – Full‑featured GUI application built with **Tkinter**, persisting user records in **SQLite**, and visualising BMI trends using **Matplotlib**.
* **Phase 3 – QA, Cleanup & Submission Documentation** – Code cleanup, testing, and documentation.

The final implementation is ready for submission.

## Features

* **BMI calculation** using the standard formula `BMI = weight / (height ** 2)`.
* Classification into **Underweight, Normal, Overweight, Obese**.
* Multi‑user support – each user’s measurements are stored separately.
* **SQLite** (`bmi_records.db`) persistence of weight, height, BMI and calculation date.
* **Tkinter** GUI with:
  * Input fields for user name, weight (kg) and height (m).
  * Color‑coded BMI result badge.
  * History table showing past records.
  * Matplotlib line‑graph displaying BMI trends over time.
* Comprehensive unit and integration tests.

## Technology Stack

* **Python 3.10+** (standard library).
* **Tkinter** – native GUI toolkit.
* **SQLite3** – lightweight relational database (standard library).
* **Matplotlib** – for BMI trend visualisation (only external dependency).

## Installation

1. Clone the repository (once it is pushed to GitHub).
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   ```
3. Install the required package:
   ```bash
   pip install -r requirements.txt
   ```
   `requirements.txt` currently contains:
   ```text
   matplotlib
   ```

## Running the Application

```bash
python bmi_gui.py
```

The GUI will launch, allowing you to create new users, record BMI measurements, view history and see a trend graph.

## Usage Guide

1. **Select or create a user** from the drop‑down list.
2. Enter **weight** (kg) and **height** (m).
3. Click **Calculate** – the BMI value and category appear, colour‑coded.
4. Click **Save Record** to store the measurement.
5. The **History** table updates with the new entry.
6. Click **Show Trend** to view a Matplotlib line chart of BMI over time for the selected user.

## Project Structure

```
BMI Calculator/
├─ .gitignore                # Git ignore rules
├─ bmi_calculator.py        # Phase 1 command‑line version (kept for reference)
├─ bmi_gui.py                # Tkinter GUI application (Phase 2)
├─ database.py               # SQLite helper module
├─ requirements.txt          # Python dependencies (matplotlib)
├─ README.md                 # This file
├─ bmi_records.db            # SQLite database (sample data)
├─ screenshots/              # Optional UI screenshots
└─ __pycache__/              # Ignored by Git
```

## Testing

Automated tests are located in the `scratch/` directory (generated during development). To run them:

```bash
python -m unittest discover -s scratch
```

All tests should pass.

## License

This project is provided for educational purposes as part of the OASIS Infobyte internship and does not carry a formal open‑source license.
