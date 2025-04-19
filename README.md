# KAG Tools - Facebook Account Creator

## Project Overview

**KAG Tools** is a GUI-based tool designed to automate the creation of Facebook accounts. The application uses `tkinter` for the GUI, `selenium` to automate browser interactions, and `openpyxl` to store account details in an Excel file. It incorporates random data generation to create realistic account profiles.

---

## File Structure

- ### `main.py`
    - The entry point of the application. It initializes the **KAG Tools** GUI and the required directories.

- ### `kag_tools.py`
    - Defines the GUI (`tkinter`) for the application.
    - Handles user inputs for account details, random data generation, and integrates account creation functionality.

- ### `data_generator.py`
    - Contains static methods for generating realistic random data (e.g., names, emails, passwords, and more).

- ### `account_creator.py`
    - Performs the browser automation using `selenium`.
    - Interacts with Facebook's registration form to create new accounts, simulates real user input, and saves session cookies.

- ### `file_handlers.py`
    - Manages saving account data to an Excel file using `openpyxl`.

---

## Workflow

### 1. **Application Startup (`main.py`)**
- Necessary directories are created: `cookies`, `data`, and `drivers`.
- The **KAG Tools** GUI is initialized and displayed to the user.

---

### 2. **User Interacts with the GUI**
- The GUI (handled in `kag_tools.py`) provides fields for user input including:
    - Full Name
    - Email
    - Password
    - Number of Accounts to Create
    - Proxy (Optional)
    - Date of Birth (Dropdown fields)
    - Gender (Radio buttons)
    - Checkbox for Headless Mode (Run Browser without UI)
- Users can either:
    - Input data manually.
    - Generate random data for the required fields using the random data generation button.

---

### 3. **Random Data Generation (`data_generator.py`)**
- When the user presses the "Generate Random Data" button:
    - The `DataGenerator` class generates:
        - Random names, emails, passwords, and other details.
    - The data is populated into the respective input fields on the GUI.

---

### 4. **Account Creation Process**
- **Start Account Creation (`kag_tools.py:_create_accounts_process`)**:
    - Based on user inputs, the program initiates a threaded process that iterates over the number of accounts to create (`account_count`).
    - For each account:
        - Calls `account_creator.py:create_account()` to interact with the Facebook registration page via `selenium`.
        - Uses the `file_handlers.py` module to save each created account's data into an Excel file.

- **Automation Workflow (`account_creator.py`)**:
    - Opens Facebook's registration page using `selenium`.
    - Simulates realistic typing for form fields:
        - First name, last name, email, password, etc.
    - Sets DOB, gender, and proxy if provided.
    - Creates the account by submitting the form.
    - If cookies are generated, they are automatically saved in the `cookies/` directory.

---

### 5. **Data Storage (Excel)**
- For successful account creations:
    - Data is appended to the Excel file `data/accounts.xlsx`.
    - Saved data includes:
        - Name
        - Email
        - Password
        - Date of Birth (DOB)
        - Gender
        - Optional Proxy
        - Timestamp of creation.

---

## Project File Map

| File/Directory      | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `main.py`           | Entry point to the project. Initializes the application.                   |
| `kag_tools.py`      | Defines the GUI, handles form validation, and orchestrates account creation processes. |
| `data_generator.py` | Provides utility methods to generate random user data for Facebook accounts.|
| `account_creator.py`| Handles browser automation using `selenium` to create Facebook accounts.   |
| `file_handlers.py`  | Saves account data to Excel (`accounts.xlsx`) for record-keeping.          |
| `data/`             | Directory to store generated Excel reports including account details.      |
| `cookies/`          | Stores cookies from successfully created accounts.                        |
| `drivers/`          | Directory to include `chromedriver` used by `selenium`.                   |

---

## Prerequisites

- Python 3.8.3 or later.
- Installed Python libraries:
  ```bash
  pip install selenium openpyxl
  ```
- Chrome browser and matching `chromedriver`. Ensure the driver is in the `/drivers` directory.

---

## How to Run

1. Clone this repository and navigate to the project folder.
2. Install required Python libraries:
   ```bash
   pip install selenium openpyxl
   ```
3. Place your `chromedriver.exe` in the `drivers` folder.
4. Run the `main.py` file to start the application:
   ```bash
   python main.py
   ```
5. Use the GUI to input or generate account details and press the **"Create Accounts"** button.

---

## Notes

- **Browsers Supported**: This project uses Google Chrome for account creation.
- **Cookies**: Saved session cookies are located in the `cookies/` directory.

---

## Disclaimer

**This project was created for learning purposes only. Automating account creation on websites (e.g., Facebook) may violate their Terms of Service (TOS). Use this tool responsibly.**