import sqlite3
import secrets

from contextlib import closing
from patient import Patient
from doctor import Doctor
from appointment import Appointment
from consultation import Consultation
from bill import Bill
from user import User
from datetime import datetime


def generate_patient_id():
    current_year = datetime.now().year
    random_hex = secrets.token_hex(3).upper()
    return f"PT-{current_year}-{random_hex}"

def generate_id(table, column, code):
    current_year = datetime.now().year
    prefix = f"{code}-{current_year}-"
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX({column}) FROM {table} WHERE {column} LIKE ?", (prefix + "%",))
        last_id = cursor.fetchone()[0]
    if last_id is None:
        return f"{prefix}001"
    last_number = int(last_id[-3:])
    return f"{prefix}{last_number + 1:03d}"

def generate_doctor_id():
    return generate_id("doctors", "doctor_id", "DR")

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
    appointment_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    doctor_id TEXT NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id))
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultations (
    consultation_id TEXT PRIMARY KEY,
    appointment_id TEXT NOT NULL UNIQUE,
    diagnosis TEXT NOT NULL,
    prescription TEXT NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id))
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bills (
    bill_id TEXT PRIMARY KEY,
    appointment_id TEXT NOT NULL UNIQUE,
    patient_id TEXT NOT NULL,
    consultation_fee REAL NOT NULL,
    medication_cost REAL NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id))
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    doctor_id TEXT)
    """)
    conn.commit()
    conn.close()

# ---------------- patients ----------------

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
        deleted = cursor.rowcount
        cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE patient_id = ? AND status = 'Scheduled'", (patient_id,))
        conn.commit()
        if deleted > 0:
            return True
        else:
            return False

def clear_all_patients():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE from patients")
        deleted = cursor.rowcount
        cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE status = 'Scheduled'")
        conn.commit()
        if deleted > 0:
            return True
        else:
            return False

# ---------------- doctors ----------------

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

def update_doctor(doctor_id, new_name, new_specialization, new_department, new_phone_number, new_email):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE doctors SET name = ?, specialization = ?, department = ?, phone_number = ?, email = ? WHERE doctor_id = ?",
        (new_name, new_specialization, new_department, new_phone_number, new_email, doctor_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

def delete_doctor(doctor_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE doctor_id = ?", (doctor_id,))
        deleted = cursor.rowcount
        cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE doctor_id = ? AND status = 'Scheduled'", (doctor_id,))
        cursor.execute("DELETE FROM users WHERE doctor_id = ?", (doctor_id,))
        conn.commit()
        if deleted > 0:
            return True
        else:
            return False

# ---------------- appointments ----------------

APPOINTMENT_QUERY = """
SELECT a.appointment_id, a.patient_id, COALESCE(p.name, '[deleted]'), a.doctor_id, COALESCE(d.name, '[deleted]'),
a.appointment_date, a.appointment_time, a.status
FROM appointments a
LEFT JOIN patients p ON a.patient_id = p.patient_id
LEFT JOIN doctors d ON a.doctor_id = d.doctor_id
"""

def row_to_appointment(row):
    return Appointment(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

def book_appointment(patient_id, doctor_id, appointment_date, appointment_time):
    new_id = generate_id("appointments", "appointment_id", "APT")
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM appointments WHERE doctor_id = ? AND appointment_date = ? AND appointment_time = ? AND status = 'Scheduled'",
        (doctor_id, appointment_date, appointment_time,))
        if cursor.fetchone() is not None:
            return None
        cursor.execute("INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, status) VALUES (?, ?, ?, ?, ?, ?)",
        (new_id, patient_id, doctor_id, appointment_date, appointment_time, "Scheduled"))
        conn.commit()
    return search_appointment(new_id)

def search_appointment(appointment_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute(APPOINTMENT_QUERY + " WHERE a.appointment_id = ?", (appointment_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return row_to_appointment(row)

def get_all_appointments():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute(APPOINTMENT_QUERY + " ORDER BY a.appointment_date, a.appointment_time")
        rows = cursor.fetchall()
        appointments_list = []
        for row in rows:
            appointments_list.append(row_to_appointment(row))
        return appointments_list

def get_doctor_appointments(doctor_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute(APPOINTMENT_QUERY + " WHERE a.doctor_id = ? ORDER BY a.appointment_date, a.appointment_time", (doctor_id,))
        rows = cursor.fetchall()
        appointments_list = []
        for row in rows:
            appointments_list.append(row_to_appointment(row))
        return appointments_list

def cancel_appointment(appointment_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE appointment_id = ? AND status = 'Scheduled'", (appointment_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

# ---------------- consultations ----------------

def complete_appointment(appointment_id, diagnosis, prescription):
    new_id = generate_id("consultations", "consultation_id", "CON")
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET status = 'Completed' WHERE appointment_id = ? AND status = 'Scheduled'", (appointment_id,))
        if cursor.rowcount == 0:
            return None
        cursor.execute("INSERT INTO consultations (consultation_id, appointment_id, diagnosis, prescription) VALUES (?, ?, ?, ?)",
        (new_id, appointment_id, diagnosis, prescription))
        conn.commit()
        consultation = Consultation(new_id, appointment_id, diagnosis, prescription)
        return consultation

# ---------------- billing ----------------

def row_to_bill(row):
    return Bill(row[0], row[1], row[2], row[3], row[4], row[5], row[6])

def appointment_has_bill(appointment_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM bills WHERE appointment_id = ?", (appointment_id,))
        if cursor.fetchone() is None:
            return False
        else:
            return True

def generate_bill(appointment_id, consultation_fee, medication_cost):
    new_id = generate_id("bills", "bill_id", "BIL")
    total = round(consultation_fee + medication_cost, 2)
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id FROM appointments WHERE appointment_id = ? AND status = 'Completed'", (appointment_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        cursor.execute("SELECT 1 FROM bills WHERE appointment_id = ?", (appointment_id,))
        if cursor.fetchone() is not None:
            return None
        cursor.execute("INSERT INTO bills (bill_id, appointment_id, patient_id, consultation_fee, medication_cost, total, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (new_id, appointment_id, row[0], consultation_fee, medication_cost, total, "Unpaid"))
        conn.commit()
        bill = Bill(new_id, appointment_id, row[0], consultation_fee, medication_cost, total, "Unpaid")
        return bill

def get_all_bills():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT bill_id, appointment_id, patient_id, consultation_fee, medication_cost, total, status FROM bills ORDER BY bill_id")
        rows = cursor.fetchall()
        bills_list = []
        for row in rows:
            bills_list.append(row_to_bill(row))
        return bills_list

def search_bill(bill_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT bill_id, appointment_id, patient_id, consultation_fee, medication_cost, total, status FROM bills WHERE bill_id = ?", (bill_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return row_to_bill(row)

def pay_bill(bill_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE bills SET status = 'Paid' WHERE bill_id = ? AND status = 'Unpaid'", (bill_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False

# ---------------- users ----------------

def count_users():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]

def create_user(username, password_hash, role, doctor_id):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash, role, doctor_id) VALUES (?, ?, ?, ?)",
            (username, password_hash, role, doctor_id))
            conn.commit()
        except sqlite3.IntegrityError:
            return None
        user = User(cursor.lastrowid, username, role, doctor_id)
        return user

def get_user_credentials(username):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, password_hash, role, doctor_id FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

def search_user(username):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, role, doctor_id FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if not row:
            return None
        user = User(row[0], row[1], row[2], row[3])
        return user

def get_all_users():
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, role, doctor_id FROM users ORDER BY user_id")
        rows = cursor.fetchall()
        users_list = []
        for row in rows:
            user = User(row[0], row[1], row[2], row[3])
            users_list.append(user)
        return users_list

def delete_user(username):
    with closing(sqlite3.connect("hospital.db")) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
