from hospital import Hospital

hospital = Hospital()

def handle_choice(choice):
     if choice == 1:
        print("Patient Registration Selected")
        patient_name = input("Enter patient's name: ").strip().upper()
        patient_age = int(input("Enter patient's Age: "))
        patient_gender = input("Enter patient's Gender: ").upper()
        new_patient = hospital.register_patient(patient_name, patient_age, patient_gender)
        new_patient.display_information()
        print("Patient registered successfully")

     elif choice == 2:
        print("Viewing Patients")
        patients_list = hospital.view_patients()
        if not patients_list:
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
         result = hospital.search_patient(search_name)
         if not result:
             print("patient not found")
         else:
             result.display_information()

     elif choice == 4:
         update_name = input("Enter patient's name to update: ").strip().upper()
         found_patient = hospital.search_patient(update_name)
         if not found_patient:
             print("patient not found")
         else:
             found_patient.display_information()
             new_name = input("Enter the new name: ").strip().upper()
             new_age  = int(input("Enter new age: "))
             new_gender = input("Enter new gender: ").strip().upper()
             hospital.update_patient(update_name, new_name, new_age, new_gender)
             print("Patient's Information updated Successfully!")

     elif choice == 5:
         delete_name = input("Enter patient's name to be deleted: ").strip().upper()
         found_patient = hospital.search_patient(delete_name)
         if not found_patient:
             print("patient not found")
         else:
             found_patient.display_information()
             confirmation = input("Are you sure you want to delete this patient? (Y/N): ")
             if confirmation.strip().upper() == "Y":
                 hospital.delete_patient(delete_name)
                 print("patient deleted successfully.")
             elif confirmation.strip().upper() == "N":
                 print("Deletion cancelled.")
             else:
                 print("Invalid option")
     elif choice == 6:
         confirmation = input("Are you sure you want to delete ALL patient records? This cannot be undone. (Y/N): ")
         if confirmation.strip().upper() == "Y":
             hospital.clear_all_patients()
             print("All patient records have been cleared.")
         elif confirmation.strip().upper() == "N":
             print("Clear cancelled.")
         else:
             print("Invalid option")

     else:
         print("Invalid Option")

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
    6. Delete patients record
    7. Exit
    """)
   try:
    choice = int(input("Enter your choice: "))
    handle_choice(choice) 
    if choice == 6:
        print("Thanks for using the system")
        break
   except ValueError:
         print("Invalid input. Please enter a number between 1 and 6.")