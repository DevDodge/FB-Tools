import os
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
            driver.get("https://temp-mail.org/en/")
            print("[⏳] Waiting for temp email to be generated...")

            # Wait until the input appears
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "mail"))
            )

            for _ in range(30):  # Max 30 attempts (~30s)
                email_input = driver.find_element(By.ID, "mail")
                temp_email = email_input.get_attribute("value")

                if temp_email and "loading" not in temp_email.lower():
                    print(f"[✔] Retrieved temporary email: {temp_email}")
                    return temp_email

                time.sleep(1)  # Wait 1s before trying again

            raise Exception("Timed out waiting for valid temp email.")

        except Exception as e:
            print(f"[✖] Error retrieving temp email: {e}")
            return None