from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def search_by_image(image_path):
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    # Uncomment the line below if you want to run in headless mode
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    
    # Initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                            options=chrome_options)
    
        # Navigate to Google Images
    driver.get("https://images.google.com/?hl=en")
    logging.info("Navigated to Google Lens")

    accept_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'L2AGLb')))  # Using the button's ID)
    accept_button.click()

    camera_icon = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Search by image" and @role="button"]')))
    camera_icon.click()

    # input
    file_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )
    
    
    # Convert to absolute path if needed
    abs_image_path = os.path.abspath(image_path)
    file_input.send_keys(abs_image_path)
    
    # Wait for the search results to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ksQYvb'))  # Use the updated class name
    )

    # Locate the divs containing the image results
    results = driver.find_elements(By.CSS_SELECTOR, 'div.ksQYvb')  # Find the correct class name for results

    valid_results = []
    # Extract and print the data attributes and image URLs
    for result in results:
        # Get the data attributes
        title = result.get_attribute('data-item-title')
        action_url = result.get_attribute('data-action-url')

        # Only consider results with a valid title
        if title:
            # Get the image URL
            try:
                image_div = result.find_element(By.CSS_SELECTOR, 'div.Me0cf')  # Locate the image div
                img = image_div.find_element(By.TAG_NAME, 'img')  # Locate the image tag
                img_src = img.get_attribute('src')  # Get the source URL of the image
            except Exception as e:
                img_src = "No image found"

            # Append to valid results
            valid_results.append({
                'title': title,
                'action_url': action_url,
                'image_url': img_src
            })

    # Display only the top 5 results
    for i, result in enumerate(valid_results[:5]):
        print(f"Result {i + 1}:\nTitle: {result['title']}\nAction URL: {result['action_url']}\nImage URL: {result['image_url']}\n")

    driver.quit()
    
    
image_path = "1.jpg"  # Replace with your image path
search_by_image(image_path)


