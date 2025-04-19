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

        random_name = f"{random.choice(first_names_en)} {random.choice(last_names_en)}"
        random_domain = random.choice(domains)
        random_email = f"{random_name.split()[0].lower()}.{random.choice(last_names_en).lower()}{random.randint(1, 99)}@{random_domain}"
        random_password = f"Pass{random.randint(1000, 9999)}"

        return {
            "name": random_name,
            "email": random_email,
            "password": random_password,
            "account_count": str(random.randint(1, 3)),
            "day": str(random.randint(1, 28)),
            "month": random.choice(["January", "February", "March", "April", "May", "June",
                                    "July", "August", "September", "October", "November", "December"]),
            "year": str(random.randint(1980, 2000)),
            "gender": random.choice(["male", "female"])
        }