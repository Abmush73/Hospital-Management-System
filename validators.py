import math
from datetime import datetime
from getpass import getpass


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


def get_valid_email(prompt):
    while True:
        email = input(prompt).strip().lower()
        if email == "":
            print("This field is required, it cannot be empty.")
        elif " " in email:
            print("Email cannot contain spaces.")
        elif email.count("@") != 1:
            print("Email must contain exactly one @.")
        else:
            local, domain = email.split("@")
            if local == "":
                print("Email must have text before the @.")
            elif "." not in domain:
                print("Email must have a dot after the @, e.g. name@hospital.com")
            elif domain.startswith(".") or domain.endswith("."):
                print("Email domain cannot start or end with a dot.")
            else:
                return email


def get_menu_choice(prompt, highest):
    while True:
        raw_choice = input(prompt).strip()
        if raw_choice == "":
            print("This field is required, it cannot be empty.")
            continue
        try:
            choice = int(raw_choice)
        except ValueError:
            print(f"Invalid choice. Please enter a number between 1 and {highest}.")
            continue
        if choice < 1 or choice > highest:
            print("Invalid choice. Please choose from the menu")
        else:
            return choice


def get_valid_date(prompt):
    while True:
        raw_date = input(prompt).strip()
        if raw_date == "":
            print("This field is required, it cannot be empty.")
            continue
        try:
            date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Use the format YYYY-MM-DD, e.g. 2026-11-20")
            continue
        if date < datetime.now().date():
            print("The date cannot be in the past.")
        else:
            return date.strftime("%Y-%m-%d")


def get_valid_time(prompt):
    while True:
        raw_time = input(prompt).strip()
        if raw_time == "":
            print("This field is required, it cannot be empty.")
            continue
        try:
            time = datetime.strptime(raw_time, "%H:%M").time()
        except ValueError:
            print("Invalid time. Use the 24-hour format HH:MM, e.g. 14:30")
            continue
        return time.strftime("%H:%M")


def get_valid_amount(prompt):
    while True:
        raw_amount = input(prompt).strip()
        if raw_amount == "":
            print("This field is required, it cannot be empty.")
            continue
        try:
            amount = float(raw_amount)
        except ValueError:
            print("Enter a valid amount, e.g. 5000 or 5000.50")
            continue
        if not math.isfinite(amount):
            print("Enter a valid amount, e.g. 5000 or 5000.50")
        elif amount < 0:
            print("Amount cannot be negative.")
        else:
            return round(amount, 2)


def get_valid_username(prompt):
    while True:
        username = input(prompt).strip().lower()
        if username == "":
            print("This field is required, it cannot be empty.")
        elif len(username) < 3:
            print("Username must be at least 3 characters.")
        elif not username.replace("_", "").isalnum():
            print("Username can only contain letters, numbers and underscores.")
        else:
            return username


def get_new_password():
    while True:
        password = getpass("Enter password: ")
        if len(password) < 6:
            print("Password must be at least 6 characters.")
            continue
        confirm = getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match, try again.")
        else:
            return password


def get_valid_role(prompt):
    while True:
        role = input(prompt).strip().lower()
        if role == "":
            print("This field is required, it cannot be empty.")
        elif role not in ("admin", "staff", "doctor"):
            print("Role must be admin, staff or doctor.")
        else:
            return role
