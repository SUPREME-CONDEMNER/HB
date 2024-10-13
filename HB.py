import os
import subprocess
import time
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Directory for Firefox profiles (this is the default path in Linux)
firefox_profiles_dir = os.path.expanduser("~/.mozilla/firefox/")

# Function to create the Firefox profiles if they don't exist
def create_firefox_profiles():
    for i in range(1, 11):
        profile_name = f"Profile{i}"
        profile_dir = f"{firefox_profiles_dir}{profile_name}"

        # Check if the profile already exists
        if not os.path.exists(profile_dir):
            print(f"Profile {profile_name} does not exist. Creating it...")
            subprocess.run(['firefox', '-CreateProfile', profile_name], check=True)
        else:
            print(f"Profile {profile_name} already exists.")

# Function to clear browser cache/history
def clear_firefox_profile(profile_name):
    profile_path = f"{firefox_profiles_dir}{profile_name}"
    cache_path = os.path.join(profile_path, "cache2")

    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
        print(f"Cache cleared for {profile_name}")
    else:
        print(f"No cache found for {profile_name}")

# Function to setup Firefox profile with custom user agent
def get_firefox_profile(profile_name, user_agent):
    profile_path = f"{firefox_profiles_dir}{profile_name}"
    options = Options()
    options.profile = profile_path
    options.set_preference("general.useragent.override", user_agent)
    return options

# Function to get a new user agent for each profile from the user agents file
def get_user_agents():
    user_agent_url = 'https://raw.githubusercontent.com/SUPREME-CONDEMNER/Useragents/refs/heads/main/user_agents_part_1.txt'
    os.system(f"wget -O user_agents.txt {user_agent_url}")
    
    with open('user_agents.txt', 'r') as f:
        user_agents = f.readlines()
    
    return [ua.strip() for ua in user_agents]

# Function to automate the interaction with websites
def automate_instance(profile_name, user_agent, instance_num):
    options = get_firefox_profile(profile_name, user_agent)
    
    # Launch Firefox browser with specific profile and user agent
    driver = webdriver.Firefox(options=options)

    try:
        # Open temp-mail.org in the first tab
        driver.get('https://temp-mail.org/')
        time.sleep(3)

        # Open hyperbeam.com in a new tab and perform actions
        driver.execute_script("window.open('https://hyperbeam.com/dashboard/', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)

        # Click image with CSS selector
        driver.find_element(By.CSS_SELECTOR, "span.styles_purpleText__rr6xz:nth-child(1)").click()
        time.sleep(2)

        # Switch back to the first tab (temp-mail)
        driver.switch_to.window(driver.window_handles[0])
        email_element = driver.find_element(By.CSS_SELECTOR, "#mail")
        email = email_element.text

        # Switch back to second tab (hyperbeam) and paste the email
        driver.switch_to.window(driver.window_handles[1])
        email_input = driver.find_element(By.CSS_SELECTOR, ".supertokens-input")
        email_input.send_keys(email)

        # Save email to Emails.txt
        with open('Emails.txt', 'a') as f:
            f.write(email + '\n')

        # Perform more actions as described...
        # For brevity, not all actions are listed here.
        
        # Finally, close the browser
        driver.quit()

    except Exception as e:
        print(f"Error during automation in profile {profile_name}: {e}")
        driver.quit()

# Main function to run 10 instances in parallel
def run_parallel_instances():
    user_agents = get_user_agents()
    
    processes = []
    
    for i in range(10):
        profile_name = f"Profile{i+1}"
        user_agent = user_agents[i]
        
        # Clear history and cache before each instance
        clear_firefox_profile(f"{profile_name}")
        
        # Run the instance in a subprocess (this is for parallel execution)
        p = subprocess.Popen(
            ['python3', 'your_script.py', profile_name, user_agent, str(i+1)], 
            shell=False
        )
        processes.append(p)
    
    # Wait for all processes to finish
    for p in processes:
        p.communicate()

if __name__ == "__main__":
    # Check and create profiles if needed
    create_firefox_profiles()
    
    # Run the instances in parallel
    run_parallel_instances()
