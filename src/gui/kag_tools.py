import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
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
        self.root.geometry("750x720")
        self.root.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        def on_enter(e, btn, color):
            btn['bg'] = color

        def on_leave(e, btn, color):
            btn['bg'] = color

        main_frame = tk.Frame(self.root, bg="#121212")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ✅ New navigation frame for back button
        nav_frame = tk.Frame(main_frame, bg="#121212")
        nav_frame.pack(fill=tk.X, anchor="w", padx=15, pady=(10, 0))


        # Title Frame (same as before)
        title_frame = tk.Frame(main_frame, bg="#121212")
        title_frame.pack(pady=(10, 20))

        title = tk.Label(
            title_frame,
            text="KAG TOOLS - Facebook Account Creator",
            font=("Segoe UI Black", 20),
            fg="#FACC15",
            bg="#121212"
        )
        title.pack()

        tk.Frame(title_frame, height=2, bg="#FACC15", width=500).pack(pady=6)

       # 🎲 Random Button
        random_btn = tk.Button(
            main_frame,
            text="🎲 توليد بيانات عشوائية",
            command=self.put_random_data_toGUI,
            bg="#10B981",
            fg="white",
            font=("Segoe UI Semibold", 12),
            padx=20,
            pady=10,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#059669"
        )
        random_btn.pack(pady=10)
        random_btn.bind("<Enter>", lambda e: on_enter(e, random_btn, "#059669"))
        random_btn.bind("<Leave>", lambda e: on_leave(e, random_btn, "#10B981"))

        # 🔲 Form Container
        form_frame = tk.Frame(main_frame, bg="#1F2937", bd=1, relief=tk.FLAT)
        form_frame.pack(pady=10, padx=30, fill=tk.X)

        # RTL Support and icons
        fields = [
            ("الاسم الكامل", "👤", "name"),
            ("البريد الإلكتروني", "📧", "email"),
            ("كلمة المرور", "🔒", "password"),
            ("عدد الحسابات", "🔢", "account_count"),
            ("البروكسي (اختياري)", "🌐", "proxy"),
        ]

        for label_text, icon, field_key in fields:
            # Create a row for the field
            row = tk.Frame(form_frame, bg="#1F2937")
            row.pack(fill=tk.X, pady=3)  # Reduce vertical spacing between rows

            # Add the label with text and icon
            label = tk.Label(
                row,
                text=f"{label_text} {icon}",
                bg="#1F2937",
                fg="#E5E7EB",
                width=22,  # Adjust width for a tighter layout
                anchor='e',  # Right-align the text
                font=("Segoe UI", 10)
            )
            label.pack(side=tk.RIGHT, padx=(5, 2))  # Reduce horizontal padding

            # Entry background frame
            entry_bg = tk.Frame(row, bg="#374151", bd=0)
            entry_bg.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=2)  # Minimize padding for alignment

            # Entry field
            entry = tk.Entry(
                entry_bg,
                font=("Segoe UI", 10),
                bg="#F9FAFB",
                fg="#111827",
                relief=tk.FLAT,
                justify="right"  # Align text to the right in the entry
            )
            entry.pack(ipady=5, ipadx=3, fill=tk.X, padx=0, pady=0)  # Tighten entry padding

            # Store the entry for later use
            self.entries[field_key] = entry
        # 📅 Date of Birth
        dob_frame = tk.Frame(form_frame, bg="#1F2937")
        dob_frame.pack(pady=6, fill=tk.X)
        tk.Label(
            dob_frame,
            text="تاريخ الميلاد 📅",  # Place the icon after the Arabic text
            width=18,
            anchor='e',  # Right-align the text and icon
            bg="#1F2937",
            fg="#E5E7EB",
            font=("Segoe UI", 10),
            justify="right"  # Ensure RTL alignment
        ).pack(side=tk.RIGHT, padx=(10, 0))

        self.day_combo = ttk.Combobox(dob_frame, width=5, values=[str(i) for i in range(1, 32)], justify='right')
        self.day_combo.pack(side=tk.RIGHT, padx=2)
        self.month_combo = ttk.Combobox(dob_frame, width=10, values=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ], justify='right')
        self.month_combo.pack(side=tk.RIGHT, padx=2)
        self.year_combo = ttk.Combobox(dob_frame, width=5, values=[str(i) for i in range(1950, 2024)], justify='right')
        self.year_combo.pack(side=tk.RIGHT, padx=2)

        # 🚻 Gender
        gender_frame = tk.Frame(form_frame, bg="#1F2937")
        gender_frame.pack(pady=6, fill=tk.X)
        tk.Label(
            gender_frame,
            text="الجنس 🚻",  # Place the icon after the Arabic text
            width=18,
            anchor='e',  # Right-align the text and icon
            bg="#1F2937",
            fg="#E5E7EB",
            font=("Segoe UI", 10),
            justify="right"  # Ensure RTL alignment
        ).pack(side=tk.RIGHT, padx=(10, 0))

        self.gender_var = tk.StringVar(value="male")
        genders = [("ذكر", "male"), ("أنثى", "female"), ("مخصص", "custom")]
        for text, val in genders:
            tk.Radiobutton(
                gender_frame,
                text=text,
                variable=self.gender_var,
                value=val,
                bg="#1F2937",
                fg="#E5E7EB",
                selectcolor="#374151",
                font=("Segoe UI", 10),
                anchor="e"
            ).pack(side=tk.RIGHT, padx=10)

        # 🕶️ Headless Checkbox
        self.headless_var = tk.BooleanVar()
        headless_check = tk.Checkbutton(
            main_frame,
            text="🕶️ تشغيل المتصفح في الخلفية (بدون عرض)",
            variable=self.headless_var,
            bg="#121212",
            fg="#F9FAFB",
            font=("Segoe UI", 10),
            selectcolor="#1F2937",
            anchor="w",
            justify="right"
        )
        headless_check.pack(pady=5)

        # ⏳ Progress
        self.progress = ttk.Progressbar(main_frame, orient='horizontal', length=320, mode='determinate')
        self.progress.pack(pady=10)

        self.status_label = tk.Label(main_frame, text="", bg="#121212", fg="#D1D5DB", font=("Segoe UI", 9),
                                     anchor="center")
        self.status_label.pack()

        self.detailed_progress_label = tk.Label(
            main_frame,
            text="يتم عرض التنبيهات هنا 📢",
            bg="#121212",
            fg="#D1D5DB",
            font=("Segoe UI", 9)
        )
        self.detailed_progress_label.pack(pady=5)

        # 🛠️ Create Button
        create_btn = tk.Button(
            main_frame,
            text="🛠️ إنشاء حسابات",
            command=self.validate_form,
            bg="#EF4444",
            fg="white",
            font=("Segoe UI Semibold", 13),
            padx=30,
            pady=12,
            bd=0,
            relief=tk.FLAT,
            cursor="hand2",
            activebackground="#DC2626"
        )
        create_btn.pack(pady=15)
        create_btn.bind("<Enter>", lambda e: on_enter(e, create_btn, "#DC2626"))
        create_btn.bind("<Leave>", lambda e: on_leave(e, create_btn, "#EF4444"))

        # 📌 Footer
        footer = tk.Label(
            main_frame,
            text="📌 تم التطوير بواسطة KAG Tools",
            bg="#121212",
            fg="#9CA3AF",
            font=("Segoe UI", 9)
        )
        footer.pack(side=tk.BOTTOM, pady=15)

    def create_form_row(self, parent, label_text, field_key):
        row = tk.Frame(parent, bg="#34495e")
        row.pack(pady=5, fill=tk.X)

        label = tk.Label(row, text=label_text, width=15, anchor='w', bg="#34495e", fg="white")
        label.pack(side=tk.LEFT)

        entry = tk.Entry(row)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.entries[field_key] = entry


    def put_random_data_toGUI(self):
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
        self.update_status("جاري إنشاء الحسابات الان...", "#4CAF50")
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
                    self.data_generator.generate_random_data()

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