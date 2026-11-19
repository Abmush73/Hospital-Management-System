import database
import auth

class Hospital:
    def __init__(self):
        database.create_tables()

    # ---------- patients ----------
    def register_patient(self, name, age, gender, phone_number, address):
        patient = database.register_patient(name, age, gender, phone_number, address)
        return patient

    def view_patients(self):
        registered_patients = database.get_all_patients()
        return registered_patients

    def search_patient(self, patient_id):
        check = database.search_patient(patient_id)
        return check

    def update_patient(self, patient_id, new_name, new_age, new_gender, new_phone_number, new_address):
        update = database.update_patient(patient_id, new_name, new_age, new_gender, new_phone_number, new_address)
        return update
        
    def delete_patient(self, patient_id):
        delete = database.delete_patient(patient_id)
        return delete

    def clear_all_patients(self):
        clear = database.clear_all_patients()
        return clear

    # ---------- doctors ----------
    def register_doctor(self, name, specialization, department, phone_number, email):
        doctor = database.register_doctor(name, specialization, department, phone_number, email)
        return doctor

    def get_all_doctors(self):
        registered_doctors = database.get_all_doctors()
        return registered_doctors

    def search_doctor(self, doctor_id):
        check = database.search_doctor(doctor_id)
        return check

    def update_doctor(self, doctor_id, new_name, new_specialization, new_department, new_phone_number, new_email):
        update = database.update_doctor(doctor_id, new_name, new_specialization, new_department, new_phone_number, new_email)
        return update

    def delete_doctor(self, doctor_id):
        delete = database.delete_doctor(doctor_id)
        return delete

    # ---------- appointments ----------
    def book_appointment(self, patient_id, doctor_id, appointment_date, appointment_time):
        appointment = database.book_appointment(patient_id, doctor_id, appointment_date, appointment_time)
        return appointment

    def get_all_appointments(self):
        appointments = database.get_all_appointments()
        return appointments

    def get_doctor_appointments(self, doctor_id):
        appointments = database.get_doctor_appointments(doctor_id)
        return appointments

    def search_appointment(self, appointment_id):
        check = database.search_appointment(appointment_id)
        return check

    def cancel_appointment(self, appointment_id):
        cancel = database.cancel_appointment(appointment_id)
        return cancel

    def complete_appointment(self, appointment_id, diagnosis, prescription):
        consultation = database.complete_appointment(appointment_id, diagnosis, prescription)
        return consultation

    # ---------- billing ----------
    def appointment_has_bill(self, appointment_id):
        check = database.appointment_has_bill(appointment_id)
        return check

    def generate_bill(self, appointment_id, consultation_fee, medication_cost):
        bill = database.generate_bill(appointment_id, consultation_fee, medication_cost)
        return bill

    def get_all_bills(self):
        bills = database.get_all_bills()
        return bills

    def search_bill(self, bill_id):
        check = database.search_bill(bill_id)
        return check

    def pay_bill(self, bill_id):
        pay = database.pay_bill(bill_id)
        return pay

    # ---------- users ----------
    def has_users(self):
        if database.count_users() > 0:
            return True
        else:
            return False

    def create_user(self, username, password, role, doctor_id):
        password_hash = auth.hash_password(password)
        user = database.create_user(username, password_hash, role, doctor_id)
        return user

    def get_all_users(self):
        users = database.get_all_users()
        return users

    def search_user(self, username):
        check = database.search_user(username)
        return check

    def delete_user(self, username):
        delete = database.delete_user(username)
        return delete
