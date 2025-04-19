import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

from selenium.webdriver.chrome.options import Options

class AccountCreator:
    def __init__(self):
        self.driver = None


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
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    const getParameter = WebGLRenderingContext.prototype.getParameter;
                    WebGLRenderingContext.prototype.getParameter = function(parameter) {
                        if (parameter === 37445) return 'Intel Inc.';
                        if (parameter === 37446) return 'Intel Iris OpenGL Engine';
                        return getParameter(parameter);
                    };
                    const toDataURL = HTMLCanvasElement.prototype.toDataURL;
                    HTMLCanvasElement.prototype.toDataURL = function() {
                        return "data:image/png;base64,fake_canvas_data";
                    };
                """
            })

            driver.get("https://www.facebook.com/r.php")

            def slow_type(element, text):
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.2))

            slow_type(driver.find_element(By.NAME, "firstname"), data['name'].split()[0])
            slow_type(driver.find_element(By.NAME, "lastname"), data['name'].split()[1])
            slow_type(driver.find_element(By.NAME, "reg_email__"), data['email'])
            time.sleep(1)
            slow_type(driver.find_element(By.NAME, "reg_passwd__"), data['password'])

            driver.find_element(By.ID, "day").send_keys(data['dob'].split()[0])
            driver.find_element(By.ID, "month").send_keys(data['dob'].split()[1])
            driver.find_element(By.ID, "year").send_keys(data['dob'].split()[2])

            gender_element = driver.find_elements(By.NAME, "sex")
            if data['gender'] == "male":
                gender_element[0].click()
            elif data['gender'] == "female":
                gender_element[1].click()

            time.sleep(3)
            driver.find_element(By.NAME, "websubmit").click()
            time.sleep(5)
            print("webSubmit clicked!")
            cookies = driver.get_cookies()
            print("Cookies retrieved!")
            email_username = data['email'].split("@")[0]
            print(f"Saving cookies for {email_username}...")
            with open(f"cookies/{email_username}_cookies.json", "w") as f:
                json.dump(cookies, f)
            return {"status": "success", "message": "Account created successfully", "cookies": cookies}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if driver:
                driver.quit()