patients_list = []
def handle_choice(choice):
     if choice == 1:
        print("Patient Registration Selected")
        patient_name = input("Enter patient's name: ")
        patient_age = int(input("Enter patient's Age: "))
        patient_gender = input("Enter patient's Gender: ")
        print(f"""Patient Registered Successfully!
                    Name: {patient_name} 
                    Age: {patient_age}
                    Gender: {patient_gender}""" )
        patient = {
                  "name": patient_name,
                  "age": patient_age,
                  "gender": patient_gender
               }
        patients_list.append(patient)    
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
                Name: {patient ["name"]}
                Age: {patient ["age"]}
                Gender: {patient ["gender"]}
                """)
     else:
         print("Invalid Option")

print("Select From The Available Options")
while True:
   print("""
    =================================
    HOSPITAL MANAGEMENT SYSTEM
    =================================

    1. Register Patient
    2. View Patients
    3. Exit
    """)
   try:
    choice = int(input("Enter your choice: "))
    handle_choice(choice) 
    if choice == 3:
        print("Thanks for using the system")
        break
   except ValueError:
         print("Invalid input. Please enter a number between 1 and 3.")

