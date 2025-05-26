import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager # Helps manage chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# --- Configuration ---
# Replace with the URL of the web page containing the video viewer
VIDEO_PAGE_URL = "https://huji.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=6ce4e7e6-ca99-474e-b78d-b2c6005def79"

# Path to your browser driver executable (e.g., chromedriver, geckodriver)
# If using webdriver_manager, you don't need to specify the path explicitly.
# DRIVER_PATH = "/path/to/your/chromedriver"

# --- Setup ---
# Configure Chrome options, especially for headless mode
chrome_options = webdriver.ChromeOptions()
# Run in headless mode (no browser window visible)
# chrome_options.add_argument("--headless")
# Optional: Add other arguments for better compatibility/stealth
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-gpu") # Often needed for headless
# chrome_options.add_argument("--window-size=1920x1080") # Set a window size
# Enable performance logging to capture network requests
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

chrome_options = Options()
chrome_options.add_experimental_option("perfLoggingPrefs", {
    "enableNetwork": True,
    "enablePage": False,
})
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--v=1')


# Initialize the browser driver
# Using webdriver_manager to automatically download and manage the driver
try:
    # service = ChromeService(executable_path=DRIVER_PATH) # Use this if specifying path manually
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Browser driver initialized successfully.")
except Exception as e:
    print(f"Error initializing browser driver: {e}")
    print("Please ensure you have the correct browser driver installed and in your PATH,")
    print("or that webdriver_manager is working correctly.")
    print("You might need to install it: pip install webdriver-manager")
    sys.exit(1)

# --- Navigation and Interaction ---
try:
    print(f"Navigating to: {VIDEO_PAGE_URL}")
    driver.get(VIDEO_PAGE_URL)

    # --- Waiting for Content ---
    # This is the most crucial part and depends heavily on the website.
    # You need to wait for the video player or the streaming content to load.
    # Examples (uncomment and adapt as needed):

    # Wait for a specific element of the video player to be visible
    # WebDriverWait(driver, 20).until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, "video")) # Example: wait for a <video> tag
    # )
    # print("Video element found.")

    # Wait for a specific amount of time (less reliable but sometimes works)
    time.sleep(10) # Wait 10 seconds for content to load

    print("Attempting to capture network requests...")

    # --- Capturing Network Requests ---
    # Accessing performance logs can be complex and browser-dependent.
    # This is a common way for Chrome, but might not work on all sites or versions.
    # You might need to explore browser-specific methods or libraries for more robust network monitoring.
    logs = driver.get_log('performance')

    m3u8_url = None
    # Iterate through the logs to find network requests
    for log in logs:
        # Log entries are typically JSON strings
        import json
        message = json.loads(log['message'])['message']
        # Look for 'Network.requestWillBeSent' events which contain request details
        if message['method'] == 'Network.requestWillBeSent':
            request_url = message['params']['request']['url']
            # Check if the URL ends with .m3u8
            if ".m3u8" in request_url.lower(): # Use .lower() for case-insensitive check
                m3u8_url = request_url
                print(f"Found potential M3U8 URL in network logs: {m3u8_url}")
                # You might find multiple, the first one might be the main playlist
                break # Stop after finding the first one, or continue to find all

    if m3u8_url:
        print("\n--- Found M3U8 URL ---")
        print(m3u8_url)
        print("----------------------")
    else:
        print("\nNo .m3u8 URL found in network logs.")
        print("Reasons could include:")
        print("- The video player hasn't loaded the stream yet.")
        print("- The stream URL is loaded differently (e.g., in JavaScript variables).")
        print("- The website uses anti-scraping measures.")
        print("- The performance logging didn't capture the request.")


except Exception as e:
    print(f"\nAn error occurred during script execution: {e}")

finally:
    # --- Cleanup ---
    if 'driver' in locals() and driver:
        print("Closing browser.")
        driver.quit()

