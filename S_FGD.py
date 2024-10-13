import os
import sys
import platform
import subprocess
import urllib.request
import tarfile
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

# Function to download and configure geckodriver
def download_geckodriver():
    system = platform.system()
    arch = platform.machine()
    
    base_url = "https://github.com/mozilla/geckodriver/releases/latest/download/"

    if system == "Linux":
        if arch == "x86_64":
            gecko_url = base_url + "geckodriver-v0.35.0-linux64.tar.gz"
        else:
            gecko_url = base_url + "geckodriver-v0.35.0-linux32.tar.gz"
    elif system == "Darwin":
        gecko_url = base_url + "geckodriver-v0.35.0-macos.tar.gz"
    elif system == "Windows":
        if arch == "AMD64":
            gecko_url = base_url + "geckodriver-v0.35.0-win64.zip"
        else:
            gecko_url = base_url + "geckodriver-v0.35.0-win32.zip"
    else:
        raise Exception(f"Unsupported system: {system}")

    print(f"Downloading geckodriver from {gecko_url}...")
    file_name = gecko_url.split("/")[-1]
    
    # Downloading geckodriver
    urllib.request.urlretrieve(gecko_url, file_name)
    print(f"Downloaded {file_name}")
    
    # Extracting geckodriver
    if file_name.endswith(".tar.gz"):
        with tarfile.open(file_name, "r:gz") as tar:
            tar.extractall()
        gecko_driver = "geckodriver"
    elif file_name.endswith(".zip"):
        with zipfile.ZipFile(file_name, "r") as zip_ref:
            zip_ref.extractall()
        gecko_driver = "geckodriver.exe"
    
    print("Geckodriver extracted.")

    # Moving geckodriver to a location in PATH
    current_path = os.getcwd()
    gecko_path = os.path.join(current_path, gecko_driver)
    
    if system == "Windows":
        # Adding geckodriver to PATH on Windows
        path_var = os.environ.get("PATH", "")
        if current_path not in path_var:
            os.environ["PATH"] = current_path + ";" + path_var
    else:
        # Moving geckodriver to /usr/local/bin or /usr/bin for Unix-like systems
        try:
            os.chmod(gecko_path, 0o755)
            subprocess.run(["sudo", "mv", gecko_path, "/usr/local/bin/"], check=True)
        except PermissionError:
            print("Permission denied! Run the script with elevated privileges to move geckodriver.")
            sys.exit(1)

    print("Geckodriver is configured successfully.")

def main():
    # Step 1: Install Selenium
    install_selenium()
    
    # Step 2: Download and configure Geckodriver
    download_geckodriver()

if __name__ == "__main__":
    main()
