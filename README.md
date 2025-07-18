# Student Admission Form Automation

This project automates the process of filling individual admission forms for students using data from an Excel sheet and student photos from Google Drive links. Each filled form is exported as a PDF.

## Project Structure
- `data/` - Place your Excel file and downloaded photos here
- `templates/` - Place your form template here (Word, HTML, etc.)
- `output/` - Generated PDF forms will be saved here
- `scripts/` - Python scripts for automation

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place your Excel file in the `data/` folder.
3. Place your form template in the `templates/` folder.
4. Run the main script:
   ```bash
   python scripts/main.py
   ``` 