from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Get credentials and other secrets from environment variables
username = os.getenv("ADDA_USERNAME", "kripajoym@gmail.com")
password = os.getenv("ADDA_PASSWORD", "Adda@1234567")
booking_date = os.getenv("BOOKING_DATE", "2025-03-10")
start_time = os.getenv("START_TIME", "10:00 AM")
end_time = os.getenv("END_TIME", "2:00 PM")

# Configure WebDriver (make sure to use the right driver for your browser)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode for Azure Pipeline
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    # Step 1: Login to ADDA
    driver.get("https://adda.io/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "loginEmail")))
    driver.find_element(By.ID, "loginEmail").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
    time.sleep(3)

    # Step 2: Navigate to Facilities and Select SEQUEL ACADEMY
    driver.get("https://adda.io/facilities")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "SEQUEL ACADEMY"))).click()
    time.sleep(2)
    
    # Step 3: Go to Event Booking
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Booking"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Event Booking"))).click()
    time.sleep(2)
    
    # Step 4: Fill Booking Form
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Book Now"))).click()
    time.sleep(2)

    # Select Event Type
    event_type_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@name='eventType']")))
    event_type_dropdown.click()
    event_type_dropdown.find_element(By.XPATH, "//option[text()='Field Trip']").click()
    time.sleep(1)

    # Select Booking Date
    date_input = driver.find_element(By.NAME, "bookingDate")
    date_input.clear()
    date_input.send_keys(booking_date)
    time.sleep(1)

    # Select Start Time
    start_time_input = driver.find_element(By.NAME, "startTime")
    start_time_input.clear()
    start_time_input.send_keys(start_time)
    time.sleep(1)

    # Select End Time
    end_time_input = driver.find_element(By.NAME, "endTime")
    end_time_input.clear()
    end_time_input.send_keys(end_time)
    time.sleep(1)

    # Check Availability
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Check Availability']"))).click()
    time.sleep(3)

    # Confirm Booking if Available
    confirm_button = driver.find_element(By.XPATH, "//button[text()='Confirm Booking']")
    if confirm_button.is_displayed():
        confirm_button.click()
        time.sleep(2)
        print("Booking confirmed successfully!")
    else:
        print("Facility not available for the selected date and time.")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    driver.quit()
