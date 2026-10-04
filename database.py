import sqlite3
import secrets
from contextlib import closing
from patient import Patient
from datetime import datetime

def generate_patient_id():
    current_year = datetime.now().year
    random_hex = secrets.token_hex(3).upper()
    return f"PT-{current_year}-{random_hex}"

def create_table():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

def register_patient(name, age, gender):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        while True:
            new_id = generate_patient_id()
            cursor.execute("SELECT 1 FROM patients WHERE patient_id = ?", (new_id,))
            if cursor.fetchone() is None:
               break

        cursor.execute("INSERT INTO patients (patient_id, name, age, gender) VALUES (?, ?, ?, ?)", (new_id, name, age, gender))
        conn.commit()
        patient = Patient(new_id, name, age, gender)
        return patient
    
def get_all_patients():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id, name, age, gender FROM patients")
        rows = cursor.fetchall()
        patients_list = []
        for row in rows:
            patient = Patient(row[0], row[1], row[2], row[3])
            patients_list.append(patient)
        return patients_list

def search_patient(patient_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id, name, age, gender FROM patients WHERE patient_id=?", (patient_id,))
        row = cursor.fetchone()
        if not row:
            return None
        patient = Patient(row[0], row[1], row[2], row[3])
        return patient

def update_patient(patient_id, new_name, new_age, new_gender):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET name = ?, age = ?, gender = ? WHERE patient_id = ?", (new_name, new_age, new_gender, patient_id,))
        conn.commit()
        confirm = cursor.rowcount
        if confirm > 0:
            return True
        else:
            return False

def delete_patient(patient_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

def clear_all_patients():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE from patients")
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False