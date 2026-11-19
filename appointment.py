class Appointment:
    def __init__(self, appointment_id, patient_id, patient_name, doctor_id, doctor_name, appointment_date, appointment_time, status):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status

    def display_information(self):
        print(f"""
    Appointment Information
    -----------------------
    ID: {self.appointment_id}
    Patient: {self.patient_name} ({self.patient_id})
    Doctor: {self.doctor_name} ({self.doctor_id})
    Date: {self.appointment_date}
    Time: {self.appointment_time}
    Status: {self.status}
    """)
