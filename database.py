import sqlite3
import secrets

from contextlib import closing
from patient import Patient
from doctor import Doctor
from datetime import datetime


def generate_patient_id():
    current_year = datetime.now().year
    random_hex = secrets.token_hex(3).upper()
    return f"PT-{current_year}-{random_hex}"

def  generate_doctor_id():
    current_year = datetime.now().year
    prefix = f"DR-{current_year}-"
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM doctors WHERE doctor_id LIKE ?", (prefix + "%",))
        count = cursor.fetchone()[0]
        return f"{prefix}{count + 1:03d}"

def create_tables():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    address TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
    doctor_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    department TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

def register_patient(name, age, gender, phone_number, address):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        while True:
            new_id = generate_patient_id()
            cursor.execute("SELECT 1 FROM patients WHERE patient_id = ?", (new_id,))
            if cursor.fetchone() is None:
               break

        cursor.execute("INSERT INTO patients (patient_id, name, age, gender, phone_number, address) VALUES (?, ?, ?, ?, ?, ?)", 
        (new_id, name, age, gender, phone_number, address))
        conn.commit()
        patient = Patient(new_id, name, age, gender, phone_number, address)
        return patient
    
def get_all_patients():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id, name, age, gender, phone_number, address FROM patients")
        rows = cursor.fetchall()
        patients_list = []
        for row in rows:
            patient = Patient(row[0], row[1], row[2], row[3], row[4], row[5])
            patients_list.append(patient)
        return patients_list

def search_patient(patient_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id, name, age, gender, phone_number, address FROM patients WHERE patient_id=?", 
        (patient_id,))
        row = cursor.fetchone()
        if not row:
            return None
        patient = Patient(row[0], row[1], row[2], row[3], row[4], row[5])
        return patient

def update_patient(patient_id, new_name, new_age, new_gender, new_phone_number, new_address):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET name = ?, age = ?, gender = ?, phone_number = ?, address = ? WHERE patient_id = ?",
        (new_name, new_age, new_gender, new_phone_number, new_address, patient_id,))
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

def register_doctor(name, specialization, department, phone_number, email):
    with closing(sqlite3.connect("hospital.db")) as conn:
        new_id = generate_doctor_id()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors (doctor_id, name, specialization, department, phone_number, email) VALUES (?, ?, ?, ?, ?, ?)",
        (new_id, name, specialization, department, phone_number, email),)
        conn.commit()
        doctor = Doctor(new_id, name, specialization, department, phone_number, email)
        return doctor

def get_all_doctors():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT doctor_id, name, specialization, department, phone_number, email FROM doctors")
        rows = cursor.fetchall()
        doctor_list = []
        for row in rows:
            doctor = Doctor(row[0], row[1], row[2], row[3], row[4], row[5])
            doctor_list.append(doctor)
        return doctor_list

def search_doctor(doctor_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT doctor_id, name, specialization, department, phone_number, email FROM doctors WHERE doctor_id = ?",
        (doctor_id,))
        row = cursor.fetchone()
        if not row:
            return None
        doctor = Doctor(row[0], row[1], row[2], row[3], row[4], row[5])
        return doctor