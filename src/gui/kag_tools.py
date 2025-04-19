import tkinter as tk
from tkinter import ttk, messagebox
import os
import time
import random
import string
import threading
import json
from src.core.account_creator import AccountCreator
from src.core.data_generator import DataGenerator
from src.utils.file_handlers import ExcelHandler

class KagTools :
    def __init__(self, root):
        self.root = root
        self.entries = {}
        self.account_creator = AccountCreator()
        self.data_generator = DataGenerator()
        self.save_to_excel = ExcelHandler.save_to_excel
        self.root.title("KAG TOOLS")
        self.root.geometry("750x680")
        self.root.resizable(False, False)
        self.setup_ui()


    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_frame = tk.Frame(main_frame, bg="#1a1a1a")
        title_frame.pack(pady=15)

        title = tk.Label(
            title_frame,
            text="KAG TOOLS - Facebook Account Creator",
            font=("Impact", 22, "bold"),
            fg="#FFD700",
            bg="#1a1a1a",
            padx=15,
            pady=8
        )
        title.pack()

        tk.Frame(title_frame, height=3, bg="#FFD700", width=450).pack(pady=5)

        random_btn = tk.Button(
            main_frame,
            text="🎲 توليد بيانات عشوائية",
            command=self.generate_random_data,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=8,
            cursor="hand2"
        )
        random_btn.pack(pady=10)

        form_frame = tk.Frame(main_frame, bg="#34495e")
        form_frame.pack(pady=10, padx=25, fill=tk.X)

        fields = [
            ("الاسم الكامل", "name"),
            ("البريد الإلكتروني", "email"),
            ("كلمة المرور", "password"),
            ("عدد الحسابات", "account_count"),
            ("البروكسي (اختياري)", "proxy"),
        ]

        for text, field in fields:
            self.create_form_row(form_frame, text, field)

        dob_frame = tk.Frame(form_frame, bg="#34495e")
        dob_frame.pack(pady=5, fill=tk.X)

        tk.Label(
            dob_frame,
            text="تاريخ الميلاد",
            width=15,
            anchor='w',
            bg="#34495e",
            fg="white"
        ).pack(side=tk.LEFT)

        self.day_combo = ttk.Combobox(dob_frame, width=5, values=[str(i) for i in range(1, 32)])
        self.day_combo.pack(side=tk.LEFT, padx=2)

        self.month_combo = ttk.Combobox(dob_frame, width=10, values=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.month_combo.pack(side=tk.LEFT, padx=2)

        self.year_combo = ttk.Combobox(dob_frame, width=5, values=[str(i) for i in range(1950, 2024)])
        self.year_combo.pack(side=tk.LEFT, padx=2)

        gender_frame = tk.Frame(form_frame, bg="#34495e")
        gender_frame.pack(pady=5, fill=tk.X)

        tk.Label(
            gender_frame,
            text="الجنس",
            width=15,
            anchor='w',
            bg="#34495e",
            fg="white"
        ).pack(side=tk.LEFT)

        self.gender_var = tk.StringVar(value="male")
        genders = [("ذكر", "male"), ("أنثى", "female"), ("مخصص", "custom")]
        for text, val in genders:
            tk.Radiobutton(
                gender_frame,
                text=text,
                variable=self.gender_var,
                value=val,
                bg="#34495e",
                fg="white",
                selectcolor="#2c3e50"
            ).pack(side=tk.LEFT, padx=10)

        self.headless_var = tk.BooleanVar()
        headless_check = tk.Checkbutton(
            main_frame,
            text="تشغيل المتصفح في الخلفية (بدون عرض)",
            variable=self.headless_var,
            bg="#1a1a1a",
            fg="white",
            selectcolor="#2c3e50"
        )
        headless_check.pack(pady=5)

        self.progress = ttk.Progressbar(main_frame, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=10)

        self.status_label = tk.Label(main_frame, text="", bg="#1a1a1a", fg="white")
        self.status_label.pack()

        self.detailed_progress_label = tk.Label(main_frame, text="جاري إنشاء الحسابات...", bg="#1a1a1a", fg="white")
        self.detailed_progress_label.pack(pady=5)

        create_btn = tk.Button(
            main_frame,
            text="🛠️ إنشاء حسابات",
            command=self.validate_form,#here is a cannot find declaration to go to
            bg="#FF6B6B",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=25,
            pady=12,
            cursor="hand2"
        )
        create_btn.pack(pady=15)

        footer = tk.Label(
            main_frame,
            text="تم التطوير بواسطة KAG Tools",
            bg="#1a1a1a",
            fg="#FFFFFF"
        )
        footer.pack(side=tk.BOTTOM, pady=10)

    def create_form_row(self, parent, label_text, field_key):
        row = tk.Frame(parent, bg="#34495e")
        row.pack(pady=5, fill=tk.X)

        label = tk.Label(row, text=label_text, width=15, anchor='w', bg="#34495e", fg="white")
        label.pack(side=tk.LEFT)

        entry = tk.Entry(row)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.entries[field_key] = entry

    def generate_random_string(self, length=6):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def generate_random_data(self):
        random_data = self.data_generator.generate_random_data()

        self.entries['name'].delete(0, tk.END)
        self.entries['name'].insert(0, random_data['name'])
        self.entries['email'].delete(0, tk.END)
        self.entries['email'].insert(0, random_data['email'])
        self.entries['password'].delete(0, tk.END)
        self.entries['password'].insert(0, random_data['password'])
        self.entries['account_count'].delete(0, tk.END)
        self.entries['account_count'].insert(0, random_data['account_count'])
        self.entries['proxy'].delete(0, tk.END)

        self.day_combo.set(random_data['day'])
        self.month_combo.set(random_data['month'])
        self.year_combo.set(random_data['year'])
        self.gender_var.set(random_data['gender'])

    def validate_form(self):
        threading.Thread(target=self._create_accounts_process).start()

    def prepare_account_data(self):
        return {
            "name": self.entries['name'].get(),
            "email": self.entries['email'].get(),
            "password": self.entries['password'].get(),
            "dob": f"{self.day_combo.get()} {self.month_combo.get()} {self.year_combo.get()}",
            "gender": self.gender_var.get(),
            "proxy": self.entries['proxy'].get(),
            "headless": self.headless_var.get()
        }

    def _create_accounts_process(self):
        try:
            num_accounts = int(self.entries['account_count'].get().strip())
            self.progress['maximum'] = num_accounts

            for i in range(1, num_accounts + 1):
                try:
                    # Generate random data for each account creation
                    self.generate_random_data()

                    # Prepare data from the form and random generation
                    data = self.prepare_account_data()

                    # Create the account using the prepared data
                    result = self.account_creator.create_account(data)

                    self.save_to_excel(data)
                    self.update_status(f"تم إنشاء الحساب {i}", "#4CAF50")
                    self.update_detailed_progress(f"الحساب {i}/{num_accounts} مكتمل")
                    print('result is : ', result) #returns None
                    if result['status'] == 'success':
                        # Save the account data to an Excel file
                        ExcelHandler.save_to_excel(data)

                        # Save cookies if they exist
                        if 'cookies' in result:
                            email_username = data['email'].split("@")[0]
                            os.makedirs("src/cookies", exist_ok=True)
                            with open(f"src/cookies/{email_username}_cookies.json", "w") as f:
                                json.dump(result['cookies'], f)

                        # Update the status to show success
                        self.update_status(f"تم إنشاء الحساب {i}", "#4CAF50")
                    else:
                        # Update the status to show failure
                        self.update_status(f"فشل في الحساب {i}: {result['message']}", "red") # returns NoneType object is not subscriptable

                    # Update the detailed progress for the current account
                    self.update_detailed_progress(f"الحساب {i}/{num_accounts} مكتمل")
                except Exception as e:
                    # Update the status to show failure for the current account
                    self.update_status(f"فشل في الحساب {i}: {str(e)}", "red")

                # Update the progress bar
                self.progress['value'] = i
                self.root.update()
                time.sleep(random.uniform(2, 4))

            # Show a message box when all accounts have been created
            messagebox.showinfo("الانتهاء", "تمت العملية")
        except Exception as e:
            # Show a message box in case of an error
            messagebox.showerror("خطأ", str(e))

    def update_status(self, message, color):
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def update_detailed_progress(self, message):
        self.detailed_progress_label.config(text=message)
        self.root.update()

    def on_close(self):
        self.root.destroy()