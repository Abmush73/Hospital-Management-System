import os
from patient import Patient

def save_patients(patients_list):
    with open("patients_data.txt", "w") as f:
        for patient in patients_list:
            f.write(f"{patient.name},{patient.age},{patient.gender}\n")


def load_patients():
    patients_list = []
    if not os.path.exists("patients_data.txt"):
        return patients_list 
    with open("patients_data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            name, age, gender = line.split(",")
            patient = Patient(name, int(age), gender)
            patients_list.append(patient)
    return patients_list