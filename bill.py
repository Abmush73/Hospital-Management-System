class Bill:
    def __init__(self, bill_id, appointment_id, patient_id, consultation_fee, medication_cost, total, status):
        self.bill_id = bill_id
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.consultation_fee = float(consultation_fee)
        self.medication_cost = float(medication_cost)
        self.total = float(total)
        self.status = status

    def display_information(self):
        print(f"""
    Bill Information
    ----------------
    Bill ID: {self.bill_id}
    Appointment: {self.appointment_id}
    Patient ID: {self.patient_id}
    Consultation fee: NGN {self.consultation_fee:,.2f}
    Medication cost: NGN {self.medication_cost:,.2f}
    Total: NGN {self.total:,.2f}
    Status: {self.status}
    """)
