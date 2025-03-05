from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# Get credentials and other secrets from environment variables
username = os.getenv("ADDA_USERNAME")
password = os.getenv("ADDA_PASSWORD")
booking_date = os.getenv("BOOKING_DATE", "2025-03-07")
time_slot = os.getenv("TIME_SLOT", "10:00-12:00")

# Configure WebDriver (make sure to use the right driver for your browser)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode for Azure Pipeline
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    # Step 1: Login
    driver.get("https://your-adda-portal.com/login")
    time.sleep(2)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
    time.sleep(3)

    # Step 2: Navigate to Facility Booking
    driver.get("https://adda.io/login")
    time.sleep(2)

    # Step 3: Book the Facility
    driver.find_element(By.ID, "facility_id_12345").click()  # Replace with actual ID
    time.sleep(1)
    driver.find_element(By.NAME, "date").send_keys(booking_date)
    driver.find_element(By.NAME, "time_slot").send_keys(time_slot)
    driver.find_element(By.ID, "book_now").click()
    time.sleep(2)

    # Capture success message
    success_message = driver.find_element(By.CLASS_NAME, "success").text
    print(f"Booking Status: {success_message}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    driver.quit()
