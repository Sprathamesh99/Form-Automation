import os
import pandas as pd
import requests
from jinja2 import Template
import pdfkit
import re
import urllib.parse

DATA_PATH = 'data/students.csv'
TEMPLATE_PATH = 'templates/admission_form_template.html'
OUTPUT_DIR = 'output/'
PHOTO_DIR = 'data/photos/'

os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_from_gdrive(share_url, output_path):
    patterns = [
        r'drive\.google\.com\/file\/d\/([a-zA-Z0-9_-]+)',
        r'drive\.google\.com\/open\?id=([a-zA-Z0-9_-]+)',
        r'drive\.google\.com\/uc\?id=([a-zA-Z0-9_-]+)'
    ]
    file_id = None
    for pattern in patterns:
        match = re.search(pattern, share_url)
        if match:
            file_id = match.group(1)
            break
    if not file_id:
        raise ValueError("Could not extract file ID from the provided Google Drive link.")
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")

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

        # Download photo from Google Drive
        photo_filename = os.path.abspath(os.path.join(PHOTO_DIR, f"{roll_number}.jpg"))
        if not os.path.exists(photo_filename):
            try:
                download_from_gdrive(photo_url, photo_filename)
            except Exception as e:
                print(f"Error downloading photo for {name}: {e}")
                photo_filename = ''

        # Fill template
        if os.path.exists(photo_filename):
            drive, path = os.path.splitdrive(photo_filename)
            # Only encode the path part, not the drive
            encoded_path = urllib.parse.quote(path.replace(os.sep, '/'))
            photo_path = f"file:///{drive}{encoded_path}"
        else:
            photo_path = ''
        print("Photo path for PDF:", photo_path)
        print("File exists:", os.path.exists(photo_filename))
        html_content = template.render(
            name=name,
            roll_number=roll_number,
            photo_path=photo_path,
            email=email,
            phone_number=phone
        )

        # Output PDF path
        pdf_filename = os.path.join(OUTPUT_DIR, f"{roll_number}_{name.replace(' ', '_')}.pdf")

        # Convert HTML to PDF
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        options = {
            'enable-local-file-access': None
        }
        pdfkit.from_string(html_content, pdf_filename, configuration=config, options=options)
        print(f"Generated: {pdf_filename}")

if __name__ == "__main__":
    main() 