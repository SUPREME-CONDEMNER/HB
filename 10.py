import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from multiprocessing import Pool

# Set paths for geckodriver and Firefox profiles
GECKODRIVER_PATH = "/usr/local/bin/geckodriver"  # Modify this according to your geckodriver path
FIREFOX_PATH = "/usr/bin/firefox"

# URL for user agents
USER_AGENTS_URL = "https://raw.githubusercontent.com/SUPREME-CONDEMNER/Useragents/refs/heads/main/user_agents_part_1.txt"

# File paths for saving data
EMAILS_FILE = "Emails.txt"
TEST_KEYS_FILE = "Test_Keys.txt"
PROD_KEYS_FILE = "Production_Keys.txt"

# Firefox profile base directory
FIREFOX_PROFILE_BASE_DIR = os.path.expanduser("~/.mozilla/firefox")

# Fetch user agents from the given URL
def fetch_user_agents():
    response = requests.get(USER_AGENTS_URL)
    return response.text.strip().splitlines()

# Create a new Firefox profile directory if it doesn't exist
def create_firefox_profile(profile_name):
    profile_dir = os.path.join(FIREFOX_PROFILE_BASE_DIR, profile_name)
    
    if not os.path.exists(profile_dir):
        print(f"Creating Firefox profile: {profile_name}")
        os.makedirs(profile_dir)  # Create the profile directory if it doesn't exist
    
    return profile_dir

# Clear Firefox browser history and cache
def clear_firefox_profile(profile_dir):
    for subdir in ['cache2', 'storage', 'datareporting', 'safebrowsing']:
        subdir_path = os.path.join(profile_dir, subdir)
        if os.path.exists(subdir_path):
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                os.remove(file_path)

# Function to automate one instance of the script
def automate_instance(profile_index, user_agents, iteration):
    profile_name = f"Profile{profile_index + 1}"
    
    # Create Firefox profile directory if it doesn't exist
    profile_dir = create_firefox_profile(profile_name)
    
    # Clear browser history, cache, etc.
    clear_firefox_profile(profile_dir)
    
    # Configure Firefox options and set profile preferences
    options = Options()
    options.binary_location = FIREFOX_PATH
    options.add_argument(f"--profile={profile_dir}")  # Use the created profile directory
    options.set_preference("general.useragent.override", user_agents[profile_index + iteration * 10])
    
    # Start Firefox browser
    driver = webdriver.Firefox(service=Service(GECKODRIVER_PATH), options=options)
    
    try:
        # Visit temp-mail.org in the first tab
        driver.get("https://temp-mail.org/")
        time.sleep(3)
        email_element = driver.find_element(By.CSS_SELECTOR, "#mail")
        email_address = email_element.get_attribute("value")
        
        # Open hyperbeam.com in a new tab and automate the required clicks and form fills
        driver.execute_script("window.open('https://hyperbeam.com/dashboard/', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        
        # Click on the image using the provided CSS Selector
        driver.find_element(By.CSS_SELECTOR, "span.styles_purpleText__rr6xz:nth-child(1)").click()
        
        # Switch back to the first tab and copy the email address
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
        
        # Switch back to the second tab and fill the email field
        driver.switch_to.window(driver.window_handles[1])
        email_input = driver.find_element(By.CSS_SELECTOR, ".supertokens-input")
        email_input.send_keys(email_address)
        driver.find_element(By.CSS_SELECTOR, ".react-shadow-1bgare6").click()
        
        # Save the email to the Emails.txt file
        with open(EMAILS_FILE, "a") as f:
            f.write(email_address + "\n")
        
        # Refresh the first tab and handle further tasks (fetch keys, etc.)
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        time.sleep(3)
        
        # Click to access the email message and extract keys
        driver.find_element(By.CSS_SELECTOR, ".inbox-dataList > ul:nth-child(1) > li:nth-child(2) > div:nth-child(1) > a:nth-child(1) > span:nth-child(2)").click()
        time.sleep(2)
        
        # Click the link to be redirected to the second tab
        driver.find_element(By.CSS_SELECTOR, ".inbox-data-content-intro > center:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)").click()
        
        # Extract and save Test and Production keys
        driver.switch_to.window(driver.window_handles[1])
        
        test_key = driver.find_element(By.CSS_SELECTOR, ".styles_dashboard__QhivX > main:nth-child(2) > div:nth-child(2) > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > div:nth-child(1) > code:nth-child(1)").text
        with open(TEST_KEYS_FILE, "a") as f:
            f.write(test_key + "\n")
        
        driver.find_element(By.CSS_SELECTOR, ".styles_dashboard__QhivX > main:nth-child(2) > div:nth-child(2) > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2) > button:nth-child(1)").click()
        driver.switch_to.alert.accept()  # Confirm the dialog box
        
        prod_key = driver.find_element(By.CSS_SELECTOR, ".styles_tooltip__y1yUi > code:nth-child(1)").text
        with open(PROD_KEYS_FILE, "a") as f:
            f.write(prod_key + "\n")
    
    finally:
        # Close the browser
        driver.quit()

# Function to run multiple instances in parallel
def run_parallel_instances(iteration):
    user_agents = fetch_user_agents()
    num_profiles = 10
    
    with Pool(num_profiles) as pool:
        pool.starmap(automate_instance, [(i, user_agents, iteration) for i in range(num_profiles)])

if __name__ == "__main__":
    # Run the script 10 times (with 10 iterations)
    for iteration in range(10):
        run_parallel_instances(iteration)
