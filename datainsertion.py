import mysql.connector
import json
import re
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pradeep',
    'database': 'patients_data'
}

def extract_patient_details(extracted_text):
    patient_name = "Unknown"
    dob = None

    name_match = re.search(r"Patient Name\s*:\s*(.+)", extracted_text)
    if name_match:
        patient_name = name_match.group(1).strip()

    dob_match = re.search(r"DOB\s*:\s*(\d{1,2}/\d{1,2}/\d{2,4})", extracted_text)
    if dob_match:
        try:
            dob = datetime.strptime(dob_match.group(1), "%d/%m/%y").strftime("%Y-%m-%d")
        except ValueError:
            dob = None  

    return patient_name, dob

def insert_data(json_data):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        extracted_text = json_data["extracted_text"]
        patient_name, dob = extract_patient_details(extracted_text)

        cursor.execute("INSERT INTO patients (name, dob) VALUES (%s, %s)", (patient_name, dob))
        patient_id = cursor.lastrowid

        cursor.execute("INSERT INTO forms_data (patient_id, form_json) VALUES (%s, %s)", 
                       (patient_id, json.dumps(json_data)))

        conn.commit()
        print("✅ Data inserted successfully!")

    except mysql.connector.Error as e:
        print(f" MySQL Error: {e}")
    finally:
        cursor.close()
        conn.close()

try:
    with open("data.json", "r") as json_file:
        structured_data = json.load(json_file)
    insert_data(structured_data)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f" Error: {e}. Run aws_textract_ocr.py first.")
