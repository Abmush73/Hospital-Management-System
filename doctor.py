class Doctor:       
    def __init__(self, doctor_id, name, specialization, department, phone_number, email):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.department = department
        self.phone_number = phone_number
        self.email = email

    def display_information(self):
        print(f"""
        Available Doctor
        ----------------
        Doctor_id: {self.doctor_id}
        Name: {self.name}
        Specialization: {self.specialization}
        Department: {self.department}
        Phone_number: {self.phone_number}
        Email: {self.email}
        """)