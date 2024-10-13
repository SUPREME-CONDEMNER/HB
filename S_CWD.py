import os
import sys
import platform
import subprocess
import urllib.request
import zipfile

# Function to install selenium via pip
def install_selenium():
    try:
        import selenium
        print("Selenium is already installed.")
    except ImportError:
        print("Selenium not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
        print("Selenium installed successfully.")

# Function to download and configure ChromeDriver
def download_chromedriver():
    system = platform.system()
    arch = platform.machine()
    
    base_url = "https://chromedriver.storage.googleapis.com/"
    
    # Get the latest ChromeDriver version
    latest_version_url = base_url + "LATEST_RELEASE"
    latest_version = urllib.request.urlopen(latest_version_url).read().decode().strip()

    if system == "Linux":
        if arch == "x86_64":
            chromedriver_url = base_url + f"{latest_version}/chromedriver_linux64.zip"
        else:
            chromedriver_url = base_url + f"{latest_version}/chromedriver_linux32.zip"
    elif system == "Darwin":
        chromedriver_url = base_url + f"{latest_version}/chromedriver_mac64.zip"
    elif system == "Windows":
        chromedriver_url = base_url + f"{latest_version}/chromedriver_win32.zip"
    else:
        raise Exception(f"Unsupported system: {system}")

    print(f"Downloading ChromeDriver from {chromedriver_url}...")
    file_name = chromedriver_url.split("/")[-1]
    
    # Downloading ChromeDriver
    urllib.request.urlretrieve(chromedriver_url, file_name)
    print(f"Downloaded {file_name}")
    
    # Extracting ChromeDriver
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall()
    
    chromedriver = "chromedriver" if system != "Windows" else "chromedriver.exe"
    print("ChromeDriver extracted.")

    # Moving chromedriver to a location in PATH
    current_path = os.getcwd()
    chromedriver_path = os.path.join(current_path, chromedriver)
    
    if system == "Windows":
        # Adding ChromeDriver to PATH on Windows
        path_var = os.environ.get("PATH", "")
        if current_path not in path_var:
            os.environ["PATH"] = current_path + ";" + path_var
    else:
        # Moving chromedriver to /usr/local/bin or /usr/bin for Unix-like systems
        try:
            os.chmod(chromedriver_path, 0o755)
            subprocess.run(["sudo", "mv", chromedriver_path, "/usr/local/bin/"], check=True)
        except PermissionError:
            print("Permission denied! Run the script with elevated privileges to move ChromeDriver.")
            sys.exit(1)

    print("ChromeDriver is configured successfully.")

def main():
    # Step 1: Install Selenium
    install_selenium()
    
    # Step 2: Download and configure ChromeDriver
    download_chromedriver()

if __name__ == "__main__":
    main()
      
