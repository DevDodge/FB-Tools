import os
import re
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait


class TempMailOrg:
    def __init__(self):
        self.driver = None


    def get_temp_email(self, driver):
        try:
            # Navigate to the 1secmail website
            driver.get("https://www.1secmail.cc/en")
            print("[⏳] Navigated to the 1secmail website. Waiting for email...")

            # Wait until the input field is present
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html//input[@id='trsh_mail']"))
            )

            # Locate the input field using the provided XPath
            email_input = driver.find_element(By.XPATH, "/html//input[@id='trsh_mail']")

            # Wait until the field contains a valid email (not null and doesn't include 'loading')
            for _ in range(30):  # Check up to 30 times (~30 seconds max)
                temp_email = email_input.get_attribute("value")
                if temp_email and "loading" not in temp_email.lower():
                    print(f"[✔] Temporary email retrieved: {temp_email}")
                    return temp_email

                time.sleep(1)  # Wait 1s before checking again

            # If no valid email is found within the time limit, raise an exception
            raise Exception("Timed out waiting for valid temporary email.")

        except Exception as e:
            print(f"[✖] Error retrieving temporary email: {e}")
            return None

    def get_verification_code(self, driver):
        try:
            print("[⏳] Waiting for verification email...")

            # Wait until the element with the specific inner text is present
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//a[starts-with(text(), 'FB-')]"))
            )

            # Locate the element containing the verification code (starts with 'FB-')
            verification_element = driver.find_element(By.XPATH, "//a[starts-with(text(), 'FB-')]")
            full_text = verification_element.text  # Extract the full inner text
            print(f"[✔] Full text retrieved: {full_text}")

            # Extract only the numbers from the string using regex
            verification_code = re.search(r'\d+', full_text).group()  # Find the first sequence of digits
            print(f"[✔] Extracted verification code: {verification_code}")

            return verification_code

        except Exception as e:
            print(f"[✖] Error retrieving verification code: {e}")
            return None