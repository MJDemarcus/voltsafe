# VoltSafe Project
# VoltSafe Systems
> **Project Purpose:** To prevent electrical contractors from failing audits and to manage legal exposure for directors.

Electrical contractors entering Data Centres are failing audits not because they are unsafe, but because their Safety Management Systems (SMS) are generic, non-existent, or not aligned with Tier-1 expectations. VoltSafe solves this by generating site-specific, audit-ready documentation.

This project contains the Safety Management System generator.

## key Files
- **`app.py`**: The main application interface (Streamlit).
- **`voltsafe_python/`**: Backend logic for PDF generation and content.
- **`test_pdf.py`**: Script to test PDF generation without the UI.

## How to Run the App (Recommended)
This launches the web interface in your browser.

```bash
python3 -m streamlit run app.py
```

## How to Run the Test Script
This generates a sample PDF in the current directory.

```bash
python3 test_pdf.py
```

## Troubleshooting
If `streamlit` command is not found, use `python3 -m streamlit run app.py`.
