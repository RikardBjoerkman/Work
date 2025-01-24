# Ejector Label Creator

Ejector Label Creator is a Python-based GUI application designed to create PDF labels with serial numbers, dates, and product types. It uses the `tkinter` library for the user interface and `ReportLab` for generating the PDF labels. This tool simplifies the process of generating and printing labels for ejector products.

## Features

- **Auto-generate Serial Numbers:** Automatically generate serial numbers starting from a user-defined value.
- **Manual Entry:** Manually input custom serial numbers for labels.
- **Customizable Inputs:** Specify dates, product types, and the number of labels.
- **PDF Output:** Labels are generated as a PDF file and automatically opened in the default PDF viewer.
- **Themed Interface:** A user-friendly interface with a clean design, styled using `ttkthemes`.

## Requirements

- Python 3.7 or later
- Required Python packages:
  - `tkinter`
  - `ttkthemes`
  - `reportlab`
  - `Pillow`

## Setup Instructions

1. Download the project files provided to you.
2. Ensure the following additional files are available in the correct locations:
   - `Arial.ttf`: For generating labels with the Arial font.
   - `mycronic_logo.png` and `mycronic RGB.png`: Logo images for the interface.

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
