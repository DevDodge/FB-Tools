import os
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from src.core.tempMailOrg import TempMailOrg
from src.core.APIsRequest import get_last_email_content

class AccountCreator:
    def __init__(self):
        self.driver = None
        self.temp_mail = TempMailOrg()

    def create_account(self, data):
        print("Creating account...")
        driver = None
        try:
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15"
            ]

            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
            if data.get('headless'):
                chrome_options.add_argument("--headless")
            if data.get('proxy'):
                chrome_options.add_argument(f'--proxy-server={data["proxy"]}')

            service = Service(executable_path=os.path.abspath("drivers/chromedriver.exe"))
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Spoof fingerprinting
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    const getParameter = WebGLRenderingContext.prototype.getParameter;
                    WebGLRenderingContext.prototype.getParameter = function(parameter) {
                        if (parameter === 37445) return 'Intel Inc.';
                        if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                        return getParameter.call(this, parameter);
                    };
                    const toDataURL = HTMLCanvasElement.prototype.toDataURL;
                    HTMLCanvasElement.prototype.toDataURL = function() {
                        return "data:image/png;base64,fake_canvas_data";
                    };
                """
            })

            # Step 1: Get temporary email
            temp_email = self.temp_mail.get_temp_email(driver)
            if not temp_email:
                raise Exception("Failed to retrieve temporary email")
            print(f"[✔] Email received from temp-mail: {temp_email}")

            # Step 2: Override email in data
            data['email'] = temp_email
            print(f"[✔] Final email used for account: {data['username']}")

            # Step 3: Switch to a new tab for Facebook signup
            driver.execute_script("window.open('https://www.facebook.com/r.php', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])  # Facebook tab

            def slow_type(element, text):
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))

            slow_type(driver.find_element(By.NAME, "firstname"), data['name'].split()[0])
            slow_type(driver.find_element(By.NAME, "lastname"), data['name'].split()[1])
            slow_type(driver.find_element(By.NAME, "reg_email__"), data['email'])
            time.sleep(1)
            slow_type(driver.find_element(By.NAME, "reg_passwd__"), data['password'])

            day, month, year = data['dob'].split()
            driver.find_element(By.ID, "day").send_keys(day)
            driver.find_element(By.ID, "month").send_keys(month)
            driver.find_element(By.ID, "year").send_keys(year)

            gender_element = driver.find_elements(By.NAME, "sex")
            if data['gender'] == "male":
                gender_element[0].click()
            elif data['gender'] == "female":
                gender_element[1].click()
            else:
                gender_element[2].click()

            time.sleep(3)
            driver.find_element(By.NAME, "websubmit").click()
            time.sleep(5)
            print("[✔] webSubmit clicked!")

            cookies = driver.get_cookies()
            print("[✔] Cookies retrieved!")
            email_username = data['username'].split("@")[0]
            print(f"[✔] Saving cookies for: {email_username}...")

            os.makedirs("cookies", exist_ok=True)
            with open(f"cookies/{email_username}_cookies.json", "w") as f:
                json.dump(cookies, f)

            time.sleep(2)  # Wait for new tab to load
            driver.switch_to.window(driver.window_handles[0])  # Switch back to first tab
            time.sleep(1)  # Wait for tab switch

            verification_code = self.temp_mail.get_verification_code(driver)
            print('Verification code:', verification_code)

            time.sleep(2)  # Wait for new tab to load
            driver.switch_to.window(driver.window_handles[1])  # Switch back to first tab
            time.sleep(2)  # Wait for tab switch

            try:
                verification_input = driver.find_element(By.XPATH,
                                                         "//div[@id='conf_dialog_middle_components']//input[@id='code_in_cliff']")
                slow_type(verification_input, verification_code)
                time.sleep(1)
                verification_input.submit()
            except Exception as e:
                print(f"Error entering verification code: {str(e)}")

            time.sleep(200)
            return {
                "status": "success",
                "message": "Account created successfully",
                "cookies": cookies,
                "verification_code": verification_code
            }
        
            

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if driver:
                driver.quit()

