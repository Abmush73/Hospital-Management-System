from patient import Patient
import database

class Hospital:
    def __init__(self):
        database.create_tables()

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

    def register_doctor(self, name, specialization, department, phone_number, email):
        doctor = database.register_doctor(name, specialization, department, phone_number, email)
        return doctor

    def get_all_doctors(self):
        registered_doctors = database.get_all_doctors()
        return registered_doctors

    def search_doctor(self, doctor_id):
        check = database.search_doctor(doctor_id)
        return check