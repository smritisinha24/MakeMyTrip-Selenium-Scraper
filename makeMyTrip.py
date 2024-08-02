import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Setting up Chrome options
chrome_options = Options()
options = [
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features",
    "--disable-blink-features=AutomationControlled",
    "--disable-3d-apis"
]
for option in options:
    chrome_options.add_argument(option)

# Provide the path to your chromedriver
driver = webdriver.Chrome(options=chrome_options, service=Service('C:\\Program Files (x86)\\chromedriver.exe'))

# User inputs for source, destination, and date
source = "Delhi"
# source = input("Enter source city/airport: ")
# destination = input("Enter destination city/airport: ")
destination = "Mumbai"

# Input for departure date
departure_date_str = input("Enter departure date (e.g., 24 September 2024): ")
departure_date = datetime.strptime(departure_date_str, '%d %B %Y')

# Open MakeMyTrip flight search page
URL = "https://www.makemytrip.com/flights/"
driver.get(URL)
time.sleep(5)

# Close pop-up if it appears
try:
    close_popup = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#webklipper-publisher-widget-container-notification-close-div'))
    )
    close_popup.click()
except:
    pass

# Enter source city
try:
    source_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'fromCity'))
    )
    source_input.click()
    source_input_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="From"]'))
    )
    source_input_field.send_keys(source)
    time.sleep(2)

    # Select the first suggestion from the dropdown
    source_suggestion = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//li[@role="option"]'))
    )
    source_suggestion.click()
except Exception as e:
    print(f"Error entering source city: {e}")

# Enter destination city
try:
    destination_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'toCity'))
    )
    destination_input.click()
    destination_input_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="To"]'))
    )
    destination_input_field.send_keys(destination)
    time.sleep(2)

    # Select the first suggestion from the dropdown
    destination_suggestion = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//li[@role="option"]'))
    )
    destination_suggestion.click()
except Exception as e:
    print(f"Error entering destination city: {e}")

# Enter departure date
try:
    calendar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div/div[2]/div[1]/div[3]/label"))
    )
    driver.execute_script("arguments[0].click();", calendar)
    time.sleep(4)
except Exception as e:
    print(f"Error clicking on calendar: {e}")

year = departure_date.year
month = departure_date.strftime('%B')
day = str(departure_date.day)

while True:
    text = driver.find_element(By.XPATH, "(//div[@class='DayPicker-Caption'])").get_attribute('textContent')
    if f"{month} {year}" in text.strip():
        break
    else:
        next_month_button = driver.find_element(By.XPATH, "//span[@aria-label='Next Month']")
        next_month_button.click()
        time.sleep(1)  # Add a sleep to ensure the page has time to load

driver.find_element(By.XPATH, f"//p[text()='{day}']").click()
time.sleep(3)  # Wait for the click action to complete

# Click search button
try:
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Search")]'))
    )
    search_button.click()
except Exception as e:
    print(f"Error clicking search button: {e}")

time.sleep(25)  # Wait for results to load

# Scrape flight data
COUNT = 5

for i in range(1, COUNT + 1):
    try:
        block = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]'))
        )
    except:
        driver.close()  # Page closes when scraping is over
        break
    
    try:
        # Scroll into view

        driver.execute_script("arguments[0].scrollIntoView(true);", block)
        time.sleep(1)  # Wait for the scroll to complete

        # Scrape code
        fname = block.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[1]/div/p[1]').text
        fcode = block.find_element(By.CLASS_NAME, 'fliCode').text
        
        # DEPARTURE
        deptime = block.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[1]').text 
        depcity = block.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[1]/p[2]').text
    
        # ARRIVAL
        arrtime = block.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[1]').text
        arrcity = block.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[3]/p[2]').text
        duration = block.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[1]/div[3]/label/div/div/div/div[2]/p').text
        
        price = driver.find_element(By.XPATH, f'//*[@id="listing-id"]/div/div[2]/div/div[{i}]/div[1]/div[2]/div[2]/div/div/div').text
        price = price.split('\n')
        price = price[0][2:]
        
        # Print data to console
        print(f"Flight Name: {fname}")
        print(f"Flight Code: {fcode}")
        print(f"Departure City: {depcity}")
        print(f"Departure Time: {deptime}")
        print(f"Arrival City: {arrcity}")
        print(f"Arrival Time: {arrtime}")
        print(f"Duration: {duration}")
        print(f"Price: {price}")
        print("----------")
        
    except Exception as e:
        print(f"Error scraping flight {i}: {e}")
    time.sleep(2)

driver.close()
