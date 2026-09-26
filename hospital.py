from patient import Patient
from file_manager import save_patients, load_patients

class Hospital:
    def __init__(self):
        self.patients_list = load_patients()

    def register_patient(self, name, age, gender):
        patient = Patient(name, age, gender)
        self.patients_list.append(patient)
        save_patients(self.patients_list)
        return patient

    def view_patients(self):
        return self.patients_list

    def search_patient(self, name):
        for patient in self.patients_list:
            if patient.name == name:
                return patient
        return None

    def update_patient(self, name, new_name, new_age, new_gender):
        for patient in self.patients_list:
            if patient.name == name:
                patient.name = new_name
                patient.age = new_age
                patient.gender = new_gender
                save_patients(self.patients_list)
                return True
        return None
        
    def delete_patient(self, name):
        for patient in self.patients_list:
            if patient.name == name:
                self.patients_list.remove(patient)
                save_patients(self.patients_list)
                return True
        return None

    def clear_all_patients(self):
        self.patients_list = []
        save_patients(self.patients_list)