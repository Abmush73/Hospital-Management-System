class Consultation:
    def __init__(self, consultation_id, appointment_id, diagnosis, prescription):
        self.consultation_id = consultation_id
        self.appointment_id = appointment_id
        self.diagnosis = diagnosis
        self.prescription = prescription

    def display_information(self):
        print(f"""
    Consultation Information
    ------------------------
    ID: {self.consultation_id}
    Appointment: {self.appointment_id}
    Diagnosis: {self.diagnosis}
    Prescription: {self.prescription}
    """)
