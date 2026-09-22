# BMI Calculator

A Python-based BMI Calculator developed as **Task 2 of the OASIS Infobyte Python Programming Internship**.

The project evolved from a simple command-line BMI calculator into a graphical application with persistent user records and BMI trend visualization.

---

## Project Overview

The BMI Calculator calculates Body Mass Index (BMI) from a user's weight and height and classifies the result into the corresponding BMI category.

The project was developed in three phases:

### Phase 1 — Beginner Tier
A command-line BMI calculator that:
- Accepts weight and height as input
- Calculates BMI
- Determines the BMI category
- Validates user input

### Phase 2 — Advanced Tier
A graphical BMI management application built with:
- Tkinter GUI
- SQLite database persistence
- User-specific BMI records
- BMI history
- Matplotlib trend visualization
- Color-coded BMI results

### Phase 3 — QA & Documentation
- Testing and verification
- Code cleanup
- Project documentation
- Final submission preparation

---

## Features

### BMI Calculation

- Calculates BMI using weight and height
- Displays the calculated BMI value
- Classifies BMI into:
  - Underweight
  - Normal
  - Overweight
  - Obese
- Validates user input

### Graphical User Interface

The advanced version provides a Tkinter-based interface with:

- User selection and creation
- Weight input in kilograms
- Height input in meters
- BMI calculation
- Color-coded result display
- BMI history table
- Record saving
- BMI trend visualization

### Data Persistence

The application uses **SQLite** to store BMI records.

Stored information includes:

- User
- Weight
- Height
- BMI
- Calculation date

Each user's measurements can be maintained separately and retrieved through the application.

### BMI Trend Visualization

The application uses **Matplotlib** to display a line graph of BMI measurements over time for the selected user.

This allows previously recorded measurements to be viewed as a trend rather than as individual records only.

---

## BMI Formula

BMI is calculated using:

```text
BMI = weight (kg) / height² (m)