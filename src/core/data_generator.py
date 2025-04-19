import random
import string

class DataGenerator:
    @staticmethod
    def generate_random_string(length=6):  # Removed self parameter
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    @staticmethod
    def generate_random_data():  # Removed self parameter
        first_names_en = ["John", "Michael", "Sarah", "Emma", "James", "Olivia"]
        last_names_en = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]
        domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "mail.com", "protonmail.com"]

        # Generate full name
        first_name = random.choice(first_names_en)
        last_name = random.choice(last_names_en)
        random_name = f"{first_name} {last_name}"

        # Generate username - combine first and last names, make lowercase, strip spaces, and add a random number
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 99)}"

        # Generate password
        random_password = f"Pass{random.randint(1000, 9999)}"

        return {
            "name": random_name,          # Original full name
            "username": username,         # User-friendly username
            "password": random_password,
            "account_count": str(random.randint(1, 3)),
            "day": str(random.randint(1, 28)),
            "month": random.choice(["January", "February", "March", "April", "May", "June",
                                    "July", "August", "September", "October", "November", "December"]),
            "year": str(random.randint(1980, 2000)),
            "gender": random.choice(["male", "female"])
        }