class Patient:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = int(age)
        self.gender = gender

    def display_information(self):
        print(f"""
    Patient Information
    -------------------
    Name: {self.name}
    Age: {self.age}
    Gender: {self.gender}
    """)