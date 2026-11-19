class User:
    def __init__(self, user_id, username, role, doctor_id):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.doctor_id = doctor_id

    def display_information(self):
        print(f"""
    User Information
    ----------------
    Username: {self.username}
    Role: {self.role}
    Linked doctor ID: {self.doctor_id if self.doctor_id else "-"}
    """)
