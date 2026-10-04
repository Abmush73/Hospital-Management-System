class Patient:
    def __init__(self, patient_id, name, age, gender):
        self.patient_id = patient_id
        self.name = name
        self.age = int(age)
        self.gender = gender

    def display_information(self):
        print(f"""
    Patient Information
    -------------------
    ID: {self.patient_id}
    Name: {self.name}
    Age: {self.age}
    Gender: {self.gender}
    """) 
