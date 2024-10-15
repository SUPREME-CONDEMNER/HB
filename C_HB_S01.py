import os
import time
import shutil
import random
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process, Lock
import logging

# Set up logging for easier debugging
logging.basicConfig(filename='automation_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Create necessary text files if they do not exist
def create_files():
    files = ['Emails.txt', 'Test_Keys.txt', 'Production_Keys.txt']
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                pass  # Create empty files


# Fetch user agents from the provided URL
def fetch_user_agents():
    url = "https://raw.githubusercontent.com/SUPREME-CONDEMNER/Useragents/refs/heads/main/user_agents_part_1.txt"
    response = requests.get(url)
    if response.status_code == 200:
        user_agents = response.text.splitlines()
        logging.info(f"Fetched {len(user_agents)} user agents successfully.")
        return user_agents
    else:
        logging.error("Failed to fetch user agents.")
        return []


# Clear Chrome profile data (history, cache, etc.)
def clear_profile_data(profile_path):
    if os.path.exists(profile_path):
        shutil.rmtree(profile_path)
    os.makedirs(profile_path)


# Set up a Chrome profile with a given user agent using undetected-chromedriver
def setup_chrome_profile(profile_name, user_agent):
    profile_path = f"/home/{os.getlogin()}/.config/google-chrome/{profile_name}"
    clear_profile_data(profile_path)  # Clear profile data

    # Configure undetected-chromedriver with custom options
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument(f"--user-data-dir={profile_path}")  # Use separate profile for each instance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-cache")
    options.add_argument("--incognito")  # Run in incognito mode to avoid storing data
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")

    # Undetected ChromeDriver instance
    driver = uc.Chrome(options=options)
    return driver


# Perform the automation tasks with Selenium using undetected-chromedriver
def automate_profile(profile_index, user_agent, email_file, test_key_file, production_key_file, file_lock):
    profile_name = f"profile{profile_index}"
    driver = None  # Initialize driver to None

    try:
        # Step 1: Set up the browser with the profile and user agent
        driver = setup_chrome_profile(profile_name, user_agent)
        wait = WebDriverWait(driver, 20)

        # Open temp-mail.org
        driver.get("https://temp-mail.org/")
        time.sleep(random.uniform(2, 5))  # Random delay to mimic human behavior

        # Interact with elements like a real user
        email_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mail')))
        email_address = email_element.get_attribute('value')

        # Thread-safe file write for email
        with file_lock:
            with open(email_file, 'a') as f:
                f.write(email_address + '\n')

        # Open Hyperbeam Dashboard
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://hyperbeam.com/dashboard/")

        # Click on the button with CSS Selector
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.styles_purpleText__rr6xz:nth-child(1)"))).click()

        # Switch to temp-mail tab
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".inbox-dataList ul li:nth-child(2) a span:nth-child(2)"))).click()

        # Click necessary button
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".inbox-data-content-intro center table tbody tr td table tbody tr td table tbody tr td table tbody tr td a"))).click()

        # Switch to Hyperbeam tab and get keys
        driver.switch_to.window(driver.window_handles[1])

        # Extract Test Key
        test_key_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".styles_dashboard__QhivX main table tbody tr td div code")))
        test_key = test_key_element.text

        # Save Test Key thread-safely
        with file_lock:
            with open(test_key_file, 'a') as f:
                f.write(test_key + '\n')

        # Click button to get Production Key
        driver.find_element(By.CSS_SELECTOR, ".styles_dashboard__QhivX main table tbody tr td button").click()
        alert = driver.switch_to.alert
        alert.accept()

        # Extract Production Key
        production_key_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".styles_tooltip__y1yUi code")))
        production_key = production_key_element.text

        # Save Production Key thread-safely
        with file_lock:
            with open(production_key_file, 'a') as f:
                f.write(production_key + '\n')

        logging.info(f"Profile {profile_index} completed successfully.")

    except Exception as e:
        logging.error(f"Error in profile {profile_index}: {e}")
    finally:
        # Ensure that driver is quit if it was initialized
        if driver is not None:
            driver.quit()


# Run 10 instances of the script in parallel
def run_parallel_instances():
    create_files()
    user_agents = fetch_user_agents()

    email_file = 'Emails.txt'
    test_key_file = 'Test_Keys.txt'
    production_key_file = 'Production_Keys.txt'

    # Lock for thread-safe file writes
    file_lock = Lock()

    processes = []

    # Launch 10 parallel processes
    for i in range(10):
        if i < len(user_agents):
            user_agent = user_agents[i]
            p = Process(target=automate_profile, args=(i+1, user_agent, email_file, test_key_file, production_key_file, file_lock))
            processes.append(p)
            p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()


if __name__ == '__main__':
    run_parallel_instances()
