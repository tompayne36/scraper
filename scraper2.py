import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace these with your LinkedIn email and password
email = "tom@paynecentral.com"
password = "William0703"

companies = ['Zipcar', 'Uber', 'Lyft']
keywords = ['SAP', 'Python', 'Data Science']

base_url = "https://www.linkedin.com/sales/search/people?company={company}&keywords={keyword}"

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_experimental_option("prefs", {
                                "credentials_enable_service": False, "profile.password_manager_enabled": False})
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


def login(driver):
    """
    Function to login to LinkedIn Sales Navigator
    """
    driver.get("https://www.linkedin.com/login")

    # Wait for the login page to fully load
    time.sleep(5)

    # Input email and password
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(email)
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(password)

    # Submit the form
    password_input.send_keys(Keys.RETURN)

    # Wait for the Sales Navigator page to load
    time.sleep(5)

    # Check if redirected to login page and try again
    if "login" in driver.current_url:
        print("Login failed. Trying again...")
        login(driver)


driver = webdriver.Chrome(options=options)

# Log in to LinkedIn Sales Navigator
login(driver)

# Navigate to Sales Navigator home page
driver.get("https://www.linkedin.com/sales/home")

for company in companies:
    for keyword in keywords:
        search_url = base_url.format(company=company, keyword=keyword)
        driver.get(search_url)

        # Wait for the page to fully load
        time.sleep(5)

        # Extract the number of matching results using Beautiful Soup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results_element = soup.find(
            "span", string=lambda text: "results" in text)
        if results_element is not None:
            num_results = results_element.text.strip().split()[0]
            print(f"{company} - {keyword}: {num_results}")
        else:
            print(f"Error retrieving results count for {company} - {keyword}")

        # Extract the number of matching results using Selenium
        try:
            results_count_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(), 'results') or contains(text(), 'Results')]")))
            results_text = results_count_element.text
            print(f"{company} - {keyword}: {results_text}")
        except:
            print(f"Error retrieving results count for {company} - {keyword}")

        # Add the code to process the search results and perform necessary actions
        # ...

driver.quit()
