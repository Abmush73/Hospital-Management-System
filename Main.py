from getpass import getpass

import auth
from hospital import Hospital
from validators import (get_valid_name, get_valid_age, get_valid_gender, get_valid_phone, get_required_text, get_valid_email,
                        get_menu_choice, get_valid_date, get_valid_time, get_valid_amount,
                        get_valid_username, get_new_password, get_valid_role)
hospital = Hospital()

def handle_patient_choice(choice, user):
    if choice in (5, 6) and user.role != "admin":
        print("Access denied. Only an admin can do this.")
        return

    if choice == 1:
        print("Patient Registration Selected")
        patient_name = get_valid_name("Enter patient's name: ")
        patient_age = get_valid_age("Enter patient's Age: ")
        patient_gender = get_valid_gender("Enter patient's Gender (M/F): ")
        patient_phone_number = get_valid_phone("Enter patient's Phone number: ")
        patient_address = get_required_text("Enter patient's Address: ")
        new_patient = hospital.register_patient(patient_name, patient_age, patient_gender, patient_phone_number, patient_address)
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
        search_name = input("Enter patient's ID to Search: ").strip().upper()
        result = hospital.search_patient(search_name)
        if not result:
            print("patient not found")
        else:
            result.display_information()

    elif choice == 4:
        update_name = input("Enter patient's ID to update: ").strip().upper()
        found_patient = hospital.search_patient(update_name)
        if not found_patient:
            print("patient not found")
        else:
            found_patient.display_information()
            new_name = get_valid_name("Enter the new name: ")
            new_age  = get_valid_age("Enter new age: ")
            new_gender = get_valid_gender("Enter new gender (M/F): ")
            new_patient_phone_number = get_valid_phone("Enter new phone number: ")
            new_patient_address = get_required_text("Enter new patient address: ")
            hospital.update_patient(update_name, new_name, new_age, new_gender, new_patient_phone_number, new_patient_address)
            print("Patient's Information updated Successfully!")

    elif choice == 5:
        delete_name = input("Enter patient's ID to be deleted: ").strip().upper()
        found_patient = hospital.search_patient(delete_name)
        if not found_patient:
            print("patient not found")
        else:
            found_patient.display_information()
            while True:
                confirmation = input("Are you sure you want to delete this patient? (Y/N): ")
                if confirmation.strip().upper() == "Y":
                    hospital.delete_patient(delete_name)
                    print("patient deleted successfully.")
                    break
                elif confirmation.strip().upper() == "N":
                    print("Deletion cancelled.")
                    break
                else:
                    print("Invalid option. Please enter Y or N.")

    elif choice == 6:
        while True:
            confirmation = input("Are you sure you want to delete ALL patient records? This cannot be undone. (Y/N): ")
            if confirmation.strip().upper() == "Y":
                hospital.clear_all_patients()
                print("All patient records have been cleared.")
                break
            elif confirmation.strip().upper() == "N":
                print("Clear cancelled.")
                break
            else:
                print("Invalid option. Please enter Y or N")

    else:
        print("Invalid choice. Please choose from the menu")

def handle_doctor_choice(choice):
    if choice == 1:
        print("Doctor Registration Selected")
        doctor_name = get_valid_name("Enter Doctor's name: ")
        doctor_specialization = get_required_text("Enter Doctor's specialization: ")
        doctor_department = get_required_text("Enter Doctor's department: ")
        doctor_phone_number = get_valid_phone("Enter Doctor's phone number: ")
        doctor_email = get_valid_email("Enter Doctor's email: ")
        new_doctor = hospital.register_doctor(doctor_name, doctor_specialization, doctor_department, doctor_phone_number, doctor_email)        
        new_doctor.display_information()
        print("Doctor registered successfully")

    elif choice == 2:
        print("Viewing Doctors")
        doctors_list = hospital.get_all_doctors()
        if not doctors_list:
            print("No doctors have been registered yet")
        else:
            print("===== DOCTORS =====")
            for number, doctor in enumerate(doctors_list, start=1):
                print(f"""
                doctor {number}
                ----------------
                """)
                doctor.display_information()

    elif choice == 3:
        search_id = input("Enter doctor's ID to Search: ").strip().upper()
        result = hospital.search_doctor(search_id)
        if not result:
            print("Doctor not found")
        else:
            result.display_information()

    elif choice == 4:
        update_id = input("Enter doctor's ID to update: ").strip().upper()
        found_doctor = hospital.search_doctor(update_id)
        if not found_doctor:
            print("Doctor not found")
        else:
            found_doctor.display_information()
            new_name = get_valid_name("Enter the new name: ")
            new_specialization = get_required_text("Enter new specialization: ")
            new_department = get_required_text("Enter new department: ")
            new_phone_number = get_valid_phone("Enter new phone number: ")
            new_email = get_valid_email("Enter new email: ")
            hospital.update_doctor(update_id, new_name, new_specialization, new_department, new_phone_number, new_email)
            print("Doctor's information updated successfully!")

    elif choice == 5:
        delete_id = input("Enter doctor's ID to be deleted: ").strip().upper()
        found_doctor = hospital.search_doctor(delete_id)
        if not found_doctor:
            print("Doctor not found")
        else:
            found_doctor.display_information()
            confirmation = input("Are you sure you want to delete this doctor? Their scheduled appointments will be cancelled and their login removed. (Y/N): ")
            if confirmation.strip().upper() == "Y":
                hospital.delete_doctor(delete_id)
                print("Doctor deleted successfully.")
            elif confirmation.strip().upper() == "N":
                print("Deletion cancelled.")
            else:
                print("Invalid option")

    else:
        print("Invalid choice. Please choose from the menu")

def handle_appointment_choice(choice):
    if choice == 1:
        print("Book Appointment Selected")
        patient_id = input("Enter patient's ID: ").strip().upper()
        found_patient = hospital.search_patient(patient_id)
        if not found_patient:
            print("Patient not found")
        else:
            found_patient.display_information()
            doctors_list = hospital.get_all_doctors()
            if not doctors_list:
                print("No doctors have been registered yet")
            else:
                print("===== AVAILABLE DOCTORS =====")
                for doctor in doctors_list:
                    print(f"{doctor.doctor_id} - {doctor.name} ({doctor.specialization}, {doctor.department})")
                doctor_id = input("Enter doctor's ID: ").strip().upper()
                found_doctor = hospital.search_doctor(doctor_id)
                if not found_doctor:
                    print("Doctor not found")
                else:
                    appointment_date = get_valid_date("Enter appointment date (YYYY-MM-DD): ")
                    appointment_time = get_valid_time("Enter appointment time (HH:MM, 24-hour): ")
                    new_appointment = hospital.book_appointment(patient_id, doctor_id, appointment_date, appointment_time)
                    if not new_appointment:
                        print("This doctor already has an appointment at that date and time.")
                    else:
                        new_appointment.display_information()
                        print("Appointment booked successfully")

    elif choice == 2:
        print("Viewing Appointments")
        appointments_list = hospital.get_all_appointments()
        if not appointments_list:
            print("No appointments have been booked yet")
        else:
            print("===== APPOINTMENTS =====")
            for appointment in appointments_list:
                appointment.display_information()

    elif choice == 3:
        search_id = input("Enter appointment ID to Search: ").strip().upper()
        result = hospital.search_appointment(search_id)
        if not result:
            print("Appointment not found")
        else:
            result.display_information()

    elif choice == 4:
        cancel_id = input("Enter appointment ID to cancel: ").strip().upper()
        found_appointment = hospital.search_appointment(cancel_id)
        if not found_appointment:
            print("Appointment not found")
        elif found_appointment.status != "Scheduled":
            print(f"This appointment is already {found_appointment.status.lower()}, it cannot be cancelled.")
        else:
            found_appointment.display_information()
            confirmation = input("Are you sure you want to cancel this appointment? (Y/N): ")
            if confirmation.strip().upper() == "Y":
                hospital.cancel_appointment(cancel_id)
                print("Appointment cancelled successfully.")
            elif confirmation.strip().upper() == "N":
                print("Cancellation aborted.")
            else:
                print("Invalid option")

    else:
        print("Invalid choice. Please choose from the menu")

def handle_billing_choice(choice):
    if choice == 1:
        print("Generate Bill Selected")
        appointment_id = input("Enter appointment ID: ").strip().upper()
        found_appointment = hospital.search_appointment(appointment_id)
        if not found_appointment:
            print("Appointment not found")
        elif found_appointment.status != "Completed":
            print("A bill can only be generated for a completed appointment.")
        elif hospital.appointment_has_bill(appointment_id):
            print("This appointment has already been billed.")
        else:
            found_appointment.display_information()
            consultation_fee = get_valid_amount("Enter consultation fee: ")
            medication_cost = get_valid_amount("Enter medication cost (0 if none): ")
            new_bill = hospital.generate_bill(appointment_id, consultation_fee, medication_cost)
            new_bill.display_information()
            print("Bill generated successfully")

    elif choice == 2:
        print("Viewing Bills")
        bills_list = hospital.get_all_bills()
        if not bills_list:
            print("No bills have been generated yet")
        else:
            print("===== BILLS =====")
            for bill in bills_list:
                bill.display_information()

    elif choice == 3:
        search_id = input("Enter bill ID to Search: ").strip().upper()
        result = hospital.search_bill(search_id)
        if not result:
            print("Bill not found")
        else:
            result.display_information()

    elif choice == 4:
        pay_id = input("Enter bill ID to mark as paid: ").strip().upper()
        found_bill = hospital.search_bill(pay_id)
        if not found_bill:
            print("Bill not found")
        elif found_bill.status == "Paid":
            print("This bill has already been paid.")
        else:
            found_bill.display_information()
            confirmation = input("Confirm that payment has been received? (Y/N): ")
            if confirmation.strip().upper() == "Y":
                hospital.pay_bill(pay_id)
                print("Bill marked as paid.")
            elif confirmation.strip().upper() == "N":
                print("Payment not recorded.")
            else:
                print("Invalid option")

    else:
        print("Invalid choice. Please choose from the menu")

def handle_user_choice(choice, user):
    if choice == 1:
        print("Create User Selected")
        username = get_valid_username("Enter username: ")
        if hospital.search_user(username):
            print("That username is already taken.")
            return
        role = get_valid_role("Enter role (admin/staff/doctor): ")
        doctor_id = None
        if role == "doctor":
            doctor_id = input("Enter the ID of the doctor this login belongs to: ").strip().upper()
            found_doctor = hospital.search_doctor(doctor_id)
            if not found_doctor:
                print("Doctor not found. Register the doctor first.")
                return
        password = get_new_password()
        new_user = hospital.create_user(username, password, role, doctor_id)
        new_user.display_information()
        print("User created successfully")

    elif choice == 2:
        print("Viewing Users")
        users_list = hospital.get_all_users()
        print("===== USERS =====")
        for account in users_list:
            account.display_information()

    elif choice == 3:
        delete_username = get_valid_username("Enter username to delete: ")
        found_user = hospital.search_user(delete_username)
        if delete_username == user.username:
            print("You cannot delete the account you are logged in with.")
        elif not found_user:
            print("User not found")
        else:
            found_user.display_information()
            confirmation = input("Are you sure you want to delete this user? (Y/N): ")
            if confirmation.strip().upper() == "Y":
                hospital.delete_user(delete_username)
                print("User deleted successfully.")
            elif confirmation.strip().upper() == "N":
                print("Deletion cancelled.")
            else:
                print("Invalid option")

    else:
        print("Invalid choice. Please choose from the menu")

def handle_doctor_portal_choice(choice, user):
    if choice == 1:
        print("Viewing My Appointments")
        appointments_list = hospital.get_doctor_appointments(user.doctor_id)
        if not appointments_list:
            print("You have no appointments yet")
        else:
            print("===== MY APPOINTMENTS =====")
            for appointment in appointments_list:
                appointment.display_information()

    elif choice == 2:
        print("Complete Appointment Selected")
        appointment_id = input("Enter appointment ID: ").strip().upper()
        found_appointment = hospital.search_appointment(appointment_id)
        if not found_appointment or found_appointment.doctor_id != user.doctor_id:
            print("Appointment not found")
        elif found_appointment.status != "Scheduled":
            print(f"This appointment is already {found_appointment.status.lower()}.")
        else:
            found_appointment.display_information()
            diagnosis = get_required_text("Enter diagnosis: ")
            prescription = get_required_text("Enter prescription (type None if no medication): ")
            consultation = hospital.complete_appointment(appointment_id, diagnosis, prescription)
            consultation.display_information()
            print("Consultation recorded successfully")

    else:
        print("Invalid choice. Please choose from the menu")

def patient_menu(user):
    while True:
        print("PATIENT MANAGEMENT")
        print("""
        1. Register Patient
        2. View Patients
        3. Search Patient
        4. Update Patient
        5. Delete Patient
        6. Clear All Patients
        7. Back
        """)
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 7.")
            continue
        if choice == 7:
            return
        handle_patient_choice(choice, user)

def doctor_menu():
    while True:
        print("DOCTOR MANAGEMENT")
        print("""
        1. Register Docotor
        2. View Doctors
        3. Seach Doctors
        4. Update Doctor
        5. Delete Doctor
        6. Back
        """)
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 6")
            continue
        if choice == 6:
            return
        handle_doctor_choice(choice)

def appointment_menu():
    while True:
        print("APPOINTMENT MANAGEMENT")
        print("""
        1. Book Appointment
        2. View Appointments
        3. Search Appointment
        4. Cancel Appointment
        5. Back
        """)
        choice = get_menu_choice("Enter your choice: ", 5)
        if choice == 5:
            return
        handle_appointment_choice(choice)

def billing_menu():
    while True:
        print("BILLING")
        print("""
        1. Generate Bill
        2. View Bills
        3. Search Bill
        4. Mark Bill as Paid
        5. Back
        """)
        choice = get_menu_choice("Enter your choice: ", 5)
        if choice == 5:
            return
        handle_billing_choice(choice)

def user_menu(user):
    while True:
        print("USER MANAGEMENT")
        print("""
        1. Create User
        2. View Users
        3. Delete User
        4. Back
        """)
        choice = get_menu_choice("Enter your choice: ", 4)
        if choice == 4:
            return
        handle_user_choice(choice, user)

def admin_menu(user):
    while True:
        print(f"""
    ====================================
       ADMIN DASHBOARD - {user.username}
    ====================================
    1. Patients
    2. Doctors
    3. Appointments
    4. Billing
    5. Users
    6. Logout
    """)
        choice = get_menu_choice("Enter your choice: ", 6)
        if choice == 1:
            patient_menu(user)
        elif choice == 2:
            doctor_menu()
        elif choice == 3:
            appointment_menu()
        elif choice == 4:
            billing_menu()
        elif choice == 5:
            user_menu(user)
        elif choice == 6:
            return

def staff_menu(user):
    while True:
        print(f"""
    ====================================
       STAFF DASHBOARD - {user.username}
    ====================================
    1. Patients
    2. Appointments
    3. Billing
    4. Logout
    """)
        choice = get_menu_choice("Enter your choice: ", 4)
        if choice == 1:
            patient_menu(user)
        elif choice == 2:
            appointment_menu()
        elif choice == 3:
            billing_menu()
        elif choice == 4:
            return

def doctor_portal(user):
    while True:
        print(f"""
    ====================================
       DOCTOR PORTAL - {user.username}
    ====================================
    1. View My Appointments
    2. Complete an Appointment
    3. Logout
    """)
        choice = get_menu_choice("Enter your choice: ", 3)
        if choice == 3:
            return
        handle_doctor_portal_choice(choice, user)

def first_time_setup():
    print("""
    ====================================
       FIRST TIME SETUP
    ====================================
    No user accounts exist yet. Create the first admin account.
    """)
    username = get_valid_username("Enter admin username: ")
    password = get_new_password()
    hospital.create_user(username, password, "admin", None)
    print("Admin account created. You can now log in.")

def login_screen():
    attempts = 0
    while attempts < 3:
        username = input("Username: ").strip().lower()
        password = getpass("Password: ")
        user = auth.login(username, password)
        if user:
            return user
        attempts += 1
        print(f"Invalid username or password. Attempts left: {3 - attempts}")
    return None

if not hospital.has_users():
    first_time_setup()

while True:
    print("""
    ====================================
       HOSPITAL MANAGEMENT SYSTEM
    ====================================
    1. Login
    2. Exit
    """ )
    choice = get_menu_choice("Enter your choice: ", 2)
    if choice == 1:
        current_user = login_screen()
        if current_user is None:
            print("Too many failed attempts. Please try again.")
            continue
        print(f"Welcome, {current_user.username} ({current_user.role})")
        if current_user.role == "admin":
            admin_menu(current_user)
        elif current_user.role == "staff":
            staff_menu(current_user)
        elif current_user.role == "doctor":
            doctor_portal(current_user)
    elif choice == 2:
        print("Thanks for using the system")
        break
