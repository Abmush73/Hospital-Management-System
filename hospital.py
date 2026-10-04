from patient import Patient
import database

class Hospital:
    def __init__(self):
        database.create_table()

    def register_patient(self, name, age, gender):
        patient = database.register_patient(name, age, gender)
        return patient

    def view_patients(self):
        registered_patients = database.get_all_patients()
        return registered_patients

    def search_patient(self, patient_id):
        check = database.search_patient(patient_id)
        return check

    def update_patient(self, patient_id, new_name, new_age, new_gender):
        update = database.update_patient(patient_id, new_name, new_age, new_gender)
        return update
        
    def delete_patient(self, patient_id):
        delete = database.delete_patient(patient_id)
        return delete

    def clear_all_patients(self):
        clear = database.clear_all_patients()
        return clear