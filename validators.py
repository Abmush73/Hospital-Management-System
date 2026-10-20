def get_valid_name(prompt):
    while True:
        name = input(prompt).strip().upper()
        if name == "":
            print("This field is required, it cannot be empty.")
        elif not name.replace(" ", "").isalpha():
            print("Name must contain only letters.")
        else:
            return name


def get_valid_age(prompt):
    while True:
        raw_age = input(prompt).strip()
        if raw_age == "":
            print("This field is required, it cannot be empty.")
            continue
        try:
            age = int(raw_age)
            if age < 1 or age > 100:
                print("Age must be between 1-100")
            else:
                return age
        except ValueError:
            print("Only whole numbers are allowed")


def get_valid_gender(prompt):
    while True:
        gender = input(prompt).strip().upper()
        if gender == "":
            print("This field is required, it cannot be empty.")
        elif gender != "M" and gender != "F":
            print("Invalid input, enter M or F")
        else:
            return gender


def get_valid_phone(prompt):
    while True:
        phone = input(prompt).strip()
        if phone == "":
            print("This field is required, it cannot be empty.")
        elif not phone.isdigit():
            print("Phone number must contain digits only.")
        elif len(phone) != 11:
            print("Phone number must be 11 digits.")
        else:
            return phone


def get_required_text(prompt):
    while True:
        text = input(prompt).strip()
        if text == "":
            print("This field is required, it cannot be empty.")
        else:
            return text