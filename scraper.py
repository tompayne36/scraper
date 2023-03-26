import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from urllib.parse import quote


# Replace these with your LinkedIn email and password
email = "tom@paynecentral.com"
password = "William0703"

# companies = ['Zipcar', 'Uber', 'Lyft']
# keywords = ['SAP', 'Python', 'Data Science']

with open('companies.txt') as companies_file:
    companies = [line.strip() for line in companies_file]

with open('keywords.txt') as keywords_file:
    keywords = [line.strip() for line in keywords_file]

base_url = "https://www.linkedin.com/sales/search/people?company={company}&keywords={keyword}"
base_url2 = "https://www.linkedin.com/sales/search/people?company={company}&keywords={keyword}&geoIncluded=102221843"


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
        encoded_company = quote(company)
        search_url = base_url.format(company=encoded_company, keyword=keyword)
        driver.get(search_url)

        # Wait for the page to fully load
        time.sleep(20)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # Construct the screenshot file name with the timestamp
        filename = f"screenshot_{company}_{timestamp}.png"

        # Take a screenshot and save it to the file with the timestamped name
        driver.get_screenshot_as_file(filename)

        # Get page source code
        # src = driver.page_source
        # soup = BeautifulSoup(src, 'lxml')

        # Strip text from source code
        # results = soup.find('small', {
        #                    'class': 't-14 flex align-items-center ml3 pl3 _display-count-spacing_1igybl'}).get_text().strip().split()[0]
        # results = int(results.replace(',', ''))
        # print(f"{company} - {keyword}: {results}")

        # Get the HTML of the webpage
        html = driver.page_source

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html, "html.parser")

        # Find the div element with class "t-14 flex align-items-center ml3 pl3 _display-count-spacing_1igybl"
        div = soup.find(
            "div", class_="t-14 flex align-items-center ml3 pl3 _display-count-spacing_1igybl")

        # Get the text inside the span element
        span_text = div.span.text

        # Extract the integer value from the text using regular expressions
        import re
        # result_count = int(re.search(r'\d+', span_text).group())

        # Assume span_text contains the text "2k+" or "3k+", etc.
        result_count = 0
        match = re.search(r'\d+', span_text)
        if match:
            result_count = int(match.group())
        if 'K+' in span_text:
            result_count *= 1000

        # Print the result count
        # print(result_count)
        # print(f"{company} - {keyword}: {result_count}")

        search_url = base_url2.format(company=encoded_company, keyword=keyword)
        driver.get(search_url)

        # Wait for the page to fully load
        time.sleep(20)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # Construct the screenshot file name with the timestamp
        filename = f"screenshot_{company}_NA_{timestamp}.png"

        # Take a screenshot and save it to the file with the timestamped name
        driver.get_screenshot_as_file(filename)

        # Get page source code
        # src = driver.page_source
        # soup = BeautifulSoup(src, 'lxml')

        # Strip text from source code
        # results = soup.find('small', {
        #                    'class': 't-14 flex align-items-center ml3 pl3 _display-count-spacing_1igybl'}).get_text().strip().split()[0]
        # results = int(results.replace(',', ''))
        # print(f"{company} - {keyword}: {results}")

        # Get the HTML of the webpage
        html = driver.page_source

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html, "html.parser")

        # Find the div element with class "t-14 flex align-items-center ml3 pl3 _display-count-spacing_1igybl"
        div = soup.find(
            "div", class_="t-14 flex align-items-center ml3 pl3 _display-count-spacing_1igybl")

        # Get the text inside the span element
        span_text = div.span.text

        # Extract the integer value from the text using regular expressions
        import re
        # result_count = int(re.search(r'\d+', span_text).group())

        # Assume span_text contains the text "2k+" or "3k+", etc.
        result_count_NA = 0
        match = re.search(r'\d+', span_text)
        if match:
            result_count_NA = int(match.group())
        if 'K+' in span_text:
            result_count_NA *= 1000

        # Print the result count
        # print(result_count)
        print(f"{company} - {keyword}: {result_count} :: {result_count_NA}")


driver.quit()
