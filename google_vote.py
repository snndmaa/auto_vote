from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os

# Function to set up Chrome WebDriver with Incognito Mode
def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")  # Open in Incognito mode
    # options.add_argument("--headless")  # Uncomment to run in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Define the URL and button information
url = "https://ai.google.dev/competition/projects/jobgo"  # Replace with the target website URL
button_xpath = "//button[@class='gemini-voting-cta gc-analytics-event']"
new_button_class = "//button[@class='gemini-voting-cta gc-analytics-event voted"  # Replace with the new class name after clicking

# Function to click the button and wait for class change
def click_button(vote_file):
    driver = setup_driver()  # Setup the driver in Incognito mode
    driver.get(url)  # Open the webpage
    
    try:
        button = driver.find_element(By.XPATH, button_xpath)  # Locate the button
        button.click()  # Click the button
        print("Button clicked successfully!")

        # Wait for the button's class to change to the new value
        # WebDriverWait(driver, 20).until(
        #     EC.text_to_be_present_in_element_attribute((By.XPATH, button_xpath), "class", new_button_class)
        # )
        # print(f"Button class changed to: {new_button_class}")

        # # Wait an additional second after detecting the class change
        time.sleep(2.5)
        print("Waited 2.5 second after class change.")

        update_vote_count(vote_file)  # Update the vote count in the file

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # Close the browser

# Function to update the vote count in a text file
def update_vote_count(vote_file):
    # Read the current count from the file
    try:
        if os.path.exists(vote_file):
            with open(vote_file, "r") as file:
                try:
                    vote_count = int(file.read().strip())
                    print(f"Current vote count read from file: {vote_count}")
                except ValueError:
                    vote_count = 0  # If the file is empty or contains non-numeric data
                    print("File contains non-numeric data or is empty, initializing count to 0.")
        else:
            vote_count = 0  # Start at 0 if the file does not exist
            print("File does not exist. Starting vote count at 0.")

        # Increment the vote count
        vote_count += 1

        # Write the updated count back to the file
        with open(vote_file, "w") as file:
            file.write(str(vote_count))
        print(f"Updated vote count: {vote_count}")
    except Exception as e:
        print(f"An error occurred while updating the vote count file: {e}")

# List of random delays
delay_list = [1]

# File to store the vote count (use raw string to handle backslashes)
vote_file = r"C:\Users\DELL\Desktop\vote_count.txt"

# Run the script to click the button with a random delay each time
while True:
    click_button(vote_file)
    random_delay = random.choice(delay_list)  # Choose a random delay from the list
    print(f"Sleeping for {random_delay} seconds...")
    time.sleep(random_delay)  # Sleep for the random number of seconds
