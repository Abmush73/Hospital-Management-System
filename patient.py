class Patient:
    def __init__(self, patient_id, name, age, gender, phone_number , address):
        self.patient_id = patient_id
        self.name = name
        self.age = int(age)
        self.gender = gender
        self.phone_number = phone_number
        self.address = address

    def display_information(self):
        print(f"""
    Patient Information
    -------------------
    ID: {self.patient_id}
    Name: {self.name}
    Age: {self.age}
    Gender: {self.gender}
    Phone_number: {self.phone_number}
    Address: {self.address}
    """) 
