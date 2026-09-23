import os
from patient import Patient

patients_list = []

def save_patients():
    with open("patients_data.txt", "w") as f:
        for patient in patients_list:
            f.write(f"{patient.name},{patient.age},{patient.gender}\n")

def load_patients():
    if not os.path.exists("patients_data.txt"):
        return
    with open("patients_data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            name, age, gender = line.split(",")
            patient = Patient(name, int(age), gender)
            patients_list.append(patient)

def handle_choice(choice):
     if choice == 1:
        print("Patient Registration Selected")
        patient_name = input("Enter patient's name: ").strip().upper()
        patient_age = int(input("Enter patient's Age: "))
        patient_gender = input("Enter patient's Gender: ").upper()
        patient = Patient(patient_name, patient_age, patient_gender)
        print("Patient registered successfully")
        patient.display_information()
        patients_list.append(patient)
        save_patients() 

     elif choice == 2:
        print("Viewing Patients")
        if patients_list == []:
            print("No patients have been registered yet")
        else:
            print("===== PATIENTS ====")
            for number, patient in enumerate(patients_list, start=1):
                print(f"""
                patient {number}
                ----------------
                """)
                patient.display_information()

     elif choice == 3:
         search_name = input("Enter patient's Name to Search: ").strip().upper()
         found = False
         for patient in patients_list:
              if patient.name == search_name:
                 patient.display_information()
                 found = True
                 break
         if not found:
             print("patient not found")

     elif choice == 4:
         update_name = input("Enter patient's name to update: ").strip().upper()
         found = False
         for patient in patients_list:
             if patient.name == update_name:
                patient.display_information()
                new_name = input("Enter the new name: ").strip().upper()
                new_age  = int(input("Enter new age: "))
                new_gender = input("Enter new gender: ").strip().upper()
                patient.name = new_name
                patient.age = new_age
                patient.gender = new_gender
                print("Patient's Information updated Successfully!")
                save_patients()
                found = True
                break
         if not found:
                 print("patient not found")

     elif choice == 5:
         delete_name = input("Enter patient's name to be deleted: ").strip().upper()
         found = False
         for patient in patients_list:
             if patient.name == delete_name:
                 patient.display_information()
                 confirmation = input("Are you sure you want to delete this patient? (Y/N): ")
                 if confirmation.strip().upper() == "Y":
                     patients_list.remove(patient)
                     save_patients()
                     print("patient deleted successfully.")
                 elif confirmation.strip().upper() == "N":
                     print("Deletion cancelled.")
                 else:
                     print("Invalid option")
                 found = True
                 break
         if not found:
             print("patient not found.")
    
     else:
         print("Invalid Option")

load_patients()

while True:
   print("Select From The Available Options")
   print("""
    =================================
    HOSPITAL MANAGEMENT SYSTEM
    =================================

    1. Register Patient
    2. View Patients
    3. Search Patient
    4. Update Patient
    5. Delete Patient
    6. Exit
    """)
   try:
    choice = int(input("Enter your choice: "))
    handle_choice(choice) 
    if choice == 6:
        print("Thanks for using the system")
        break
   except ValueError:
         print("Invalid input. Please enter a number between 1 and 6.")