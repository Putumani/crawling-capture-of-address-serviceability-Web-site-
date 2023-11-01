import csv
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from termcolor import colored

# Function to initialize the Chrome browser
def initialize_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.binary_location = '/usr/bin/chromium-browser'  # Specify the Chrome binary location
    chrome = webdriver.Chrome(options=options)
    return chrome

# Function to process an address
def process_address(house_number, street_name, surface_code, zip_code, report_file):
    address = f"{house_number} {street_name} {surface_code}, CA {zip_code}"

    chrome = initialize_browser()
    data = {'address': address}
    data['status'] = 'UNKNOWN_ERROR'

    try:
        chrome.get("https://t-mobilefiber.com/availability/")
        time.sleep(2)  # Add a delay to allow the page to load

        # Find the address input field and enter the address
        address_input = chrome.find_element(By.ID, "address")
        address_input.send_keys(address)
        time.sleep(5)  

        # Simulate pressing the DOWN key to select the first suggestion
        address_input.send_keys(Keys.ARROW_DOWN)
        address_input.send_keys(Keys.ENTER)
        time.sleep(5)

        # Click the "Next" button
        next_button = chrome.find_element(By.XPATH, "//button[@type='submit']")
        next_button.click()
        time.sleep(10)

        # Check the current URL to determine the result
        if "/offering" in chrome.current_url:
            print(colored('Success: offering', 'green'))
            data['status'] = 'offering'
            data['currenturl'] = chrome.current_url
            log_report(report_file, data)
            save_text_dump(address, chrome.page_source)
        elif "/pre-order-offering" in chrome.current_url:
            print(colored('Success: pre-order offering', 'green'))
            data['status'] = 'pre-order offering'
            data['currenturl'] = chrome.current_url
            log_report(report_file, data)
            save_text_dump(address, chrome.page_source)
        elif "/waitlist" in chrome.current_url:
            print(colored('Waitlist', 'yellow'))
            data['status'] = 'waitlist'
            data['currenturl'] = chrome.current_url
            log_report(report_file, data)
            save_text_dump(address, chrome.page_source)
        elif "/hint/eligibility" in chrome.current_url:
            print(colored('Eligible', 'green'))
            data['status'] = 'eligible'
            data['currenturl'] = chrome.current_url
            log_report(report_file, data)
            save_text_dump(address, chrome.page_source)
        else:
            print(colored('Unknown result', 'red'))
            data['status'] = 'unknown'
            data['currenturl'] = chrome.current_url
            log_report(report_file, data)
            save_text_dump(address, chrome.page_source)

    except Exception as e:
        print(colored(f'Error: {str(e)}', 'red'))
    finally:
        chrome.quit()


def log_report(report_file, data):
    with open(report_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['address'], data['status'], data.get('currenturl', '')])

def save_text_dump(address, page_source):
    with open(f"{address.replace(' ', '_')}_text_dump.html", "w") as text_file:
        text_file.write(page_source)

def main(input_csv_file, report_csv_file, limit=3):
    with open(input_csv_file, 'r') as input_file:
        reader = csv.DictReader(input_file)
        count = 0

        for row in reader:
            house_number, street_name, surface_code, zip_code = row['HSE_NBR'], row['STR_NM'], row['STR_SFX_CD'], row['ZIP_CD']
            print(f"Processing: {house_number} {street_name} {surface_code}, {zip_code}")
            process_address(house_number, street_name, surface_code, zip_code, report_csv_file)
            count += 1

            if count >= limit:
                break

if __name__ == "__main__":
    input_csv_file = 'Addresses_in_the_City_of_Los_Angeles.csv'
    report_csv_file = 'report.csv'

    with open(report_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Address', 'Result', 'Current URL'])

    main(input_csv_file, report_csv_file, limit=10)


