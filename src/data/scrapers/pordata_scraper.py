
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os

# --- Configuration ---
# The URL of the PORDATA page with the GDP data
URL = "https://pordata.pt/portugal/produto+interno+bruto+(pib)-23"
# The directory where the downloaded file will be moved
DESTINATION_DIR = os.path.abspath("02_implementation/data_gathering/raw_data/macro")
# The expected name of the downloaded file (this might need to be adjusted)
EXPECTED_FILENAME = "pordata_gdp.xlsx"
# The full path for the final moved file.
DESTINATION_FILE = os.path.join(DESTINATION_DIR, EXPECTED_FILENAME)

def setup_driver():
    """Sets up the Chrome webdriver."""
    options = webdriver.ChromeOptions()
    # Add arguments to configure the browser for download, if needed.
    # For now, we will use the default download directory.
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

def download_gdp_data(driver, url):
    """Navigates to the URL and clicks the download button."""
    print(f"Navigating to {url}...")
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)
    
    try:
        # PORDATA uses a specific class for the Excel download icon.
        # We will try to find this element by its class name.
        print("Searching for the download button...")
        # The class name might change, so this might need updating.
        download_button = driver.find_element(By.CLASS_NAME, "ico-file-excel")
        
        print("Download button found, clicking...")
        download_button.click()
        
        # Wait for the download to complete.
        # This is a simple wait; a more robust solution would check for file existence.
        print("Waiting for the download to complete...")
        time.sleep(10)
        print("Download should be complete.")
        
    except Exception as e:
        print(f"An error occurred while trying to download the file: {e}")

def move_downloaded_file():
    """Moves the downloaded file to the correct directory."""
    # This is a placeholder for now. We need to know where the file is downloaded.
    # We will assume it's in the current working directory for now.
    # In a real-world scenario, you would configure the browser to download to a specific directory.
    # Or, you would search for the latest downloaded file in the default Downloads folder.
    if os.path.exists(EXPECTED_FILENAME):
        print(f"Moving {EXPECTED_FILENAME} to {DESTINATION_DIR}...")
        os.rename(EXPECTED_FILENAME, DESTINATION_FILE)
        print("File moved successfully.")
    else:
        print(f"Error: The expected file '{EXPECTED_FILENAME}' was not found in the current directory.")

def main():
    driver = setup_driver()
    download_gdp_data(driver, URL)
    driver.quit()
    # At this point, the file should be downloaded. Now, let's try to move it.
    # This part might fail if the file is not in the current directory.
    move_downloaded_file()

if __name__ == "__main__":
    main()
