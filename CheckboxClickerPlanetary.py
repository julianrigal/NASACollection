from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver (using Chrome in this example)
driver = webdriver.Chrome()  # Make sure ChromeDriver is in your PATH
driver.get("https://www.nasa.gov/missions/")

try:
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)

    # Step 1: Handle potential overlay (e.g., pop-ups, ads) that could block the checkbox
    try:
        overlay_close_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "selector-for-overlay-close-button")))
        overlay_close_button.click()
        print("Overlay closed.")
    except:
        print("No overlay found.")

    # Locate the checkbox for Planetary Science
    checkbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#in-mission-terms-12882")))

    # Take a screenshot before clicking
    driver.save_screenshot("before_click.png")
    print("Screenshot taken before click: 'before_click.png'")

    # Step 2: Scroll to the checkbox to bring it into view
    driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
    time.sleep(1)  # Allow time for scrolling

    # Step 3: Attempt to click the checkbox via JavaScript if normal click is intercepted
    try:
        print("Attempting to click the checkbox...")
        checkbox.click()
    except:
        # Fallback to JavaScript click if standard click is intercepted
        driver.execute_script("arguments[0].click();", checkbox)
        print("Clicked checkbox using JavaScript.")

    # Take a screenshot after clicking
    driver.save_screenshot("after_click.png")
    print("Screenshot taken after click: 'after_click.png'")

    # Step 4: Confirm if the checkbox is selected
    if checkbox.is_selected():
        print("Checkbox was successfully clicked.")
    else:
        print("Checkbox was not clicked successfully.")

    # Step 5: Count the filtered missions as validation
    time.sleep(2)  # Wait for the page to update after clicking
    mission_elements = driver.find_elements(By.CSS_SELECTOR, ".selector-for-mission-item")  # Update selector as needed
    print(f"Number of filtered missions: {len(mission_elements)}")

finally:
    # Close the browser after completing the tasks
    driver.quit()
