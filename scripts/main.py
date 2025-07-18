import os
import pandas as pd
import requests
from jinja2 import Template
import pdfkit

DATA_PATH = 'data/students.csv'
TEMPLATE_PATH = 'templates/admission_form_template.html'
OUTPUT_DIR = 'output/'
PHOTO_DIR = 'data/photos/'

os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_photo(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return filename
        else:
            return None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def main():
    # Step 1: Read CSV file
    df = pd.read_csv(DATA_PATH)

    # Step 2: Load HTML template
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = Template(f.read())

    # Step 3: Process each student
    for idx, row in df.iterrows():
        name = row['Name']
        roll_number = row['Roll Number']
        photo_url = row['Photo']
        email = row['Email']
        phone = row['Phone Number']

        # Download photo
        photo_filename = os.path.join(PHOTO_DIR, f"{roll_number}.jpg")
        if not os.path.exists(photo_filename):
            downloaded = download_photo(photo_url, photo_filename)
            if not downloaded:
                photo_filename = None

        # Fill template
        html_content = template.render(
            name=name,
            roll_number=roll_number,
            photo_path=photo_filename if photo_filename else '',
            email=email,
            phone_number=phone
        )

        # Output PDF path
        pdf_filename = os.path.join(OUTPUT_DIR, f"{roll_number}_{name.replace(' ', '_')}.pdf")

        # Convert HTML to PDF
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdfkit.from_string(html_content, pdf_filename, configuration=config)
        print(f"Generated: {pdf_filename}")

if __name__ == "__main__":
    main() 