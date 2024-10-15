import sys
import subprocess

# Function to install selenium and undetected-chromedriver via pip
def install_dependencies():
    try:
        import selenium
        import undetected_chromedriver as uc
        print("Selenium and undetected-chromedriver are already installed.")
    except ImportError:
        print("Installing Selenium and undetected-chromedriver...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "undetected-chromedriver"])
        print("Selenium and undetected-chromedriver installed successfully.")

# Function to set up and run undetected-chromedriver
def setup_undetected_chromedriver():
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    
    # Initialize undetected ChromeDriver
    print("Launching undetected ChromeDriver...")
    driver = uc.Chrome(version_main=104)  # Use version 104 of ChromeDriver
    
    # Test the driver by navigating to a website
    driver.get('https://www.google.com')
    print("Current Page Title:", driver.title)
    
    # Perform an example search on Google
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium WebDriver")
    search_box.submit()
    
    print("Search performed on Google.")
    
    # Close the driver
    driver.quit()

def main():
    # Step 1: Install Selenium and undetected-chromedriver
    install_dependencies()
    
    # Step 2: Set up and run undetected-chromedriver
    setup_undetected_chromedriver()

if __name__ == "__main__":
    main()
