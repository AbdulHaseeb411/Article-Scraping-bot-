from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time

# Set up the Selenium WebDriver with headless Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--log-level=3")  # Uncomment this line if you want headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
# chrome_options.add_argument("--headless") 
def handle_cookie_popup():
    """Handles the cookie popup by accepting or closing it."""
    try:
        consent_button = driver.find_element(By.ID, 'teal-consent-prompt-submit')  # The 'Concordo' button
        consent_button.click()
        print("Cookie popup closed by clicking 'Concordo'.")
    except Exception as e:
        print(f"No cookie popup or issue closing it: ")

def extract_urls_from_main_page(url):
    """Extracts article URLs and dates from the main page URL."""
    try:
        print(f"Loading URL: {url}")
        driver.get(url)
        handle_cookie_popup()  # Close the cookie popup
        time.sleep(5)  # Give the page time to load

        # Wait for the main elements with URLs to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tw-flex-1'))  # Adjust based on the container
        )

        all_data = []
        elements = driver.find_elements(By.CSS_SELECTOR, 'div.tw-flex-1')  # Adjust as needed

        for element in elements:
            try:
                # Check for the correct anchor tag and its class
                url_element = element.find_element(By.CSS_SELECTOR, 'a[href]')  # Ensures that we are getting anchors with href
                href = url_element.get_attribute('href')
                if href:
                    print(f"Extracted URL: {href}")

                    # Ensure the date element is correctly selected
                    date_element = element.find_element(By.TAG_NAME, 'time')
                    article_date = date_element.get_attribute('datetime')

                    if article_date:
                        print(f"Extracted Date: {article_date}")
                        all_data.append({'URL': href, 'Date': article_date})
            except Exception as e:
                print(f"???")

        return all_data

    except Exception as e:
        print(f"Error loading main page {url}: ")
        return []

def format_date(date_string):
    """Formats the date string into a datetime object."""
    try:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z").date()
    except ValueError as e:
        print(f"Date formatting error: ")
        return None

def extract_content_from_article(url):
    """Extracts the article content from the provided URL."""
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

        content_elements = driver.find_elements(By.CSS_SELECTOR, 'p span')

        article_content = ' '.join([element.text for element in content_elements if element.text.strip()])

        return article_content

    except Exception as e:
        print(f"Error extracting content from {url}:")
        return None

def scrape_url_web3(url, start_date_str, end_date_str):
    """Function that extracts URLs from the main page, filters them by date range, and extracts their content."""
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        print(f"Extracting URLs from {url}")
        urls_data = extract_urls_from_main_page(url)

        if not urls_data:
            print("No URLs found.")
            return {"message": "unsuccessful", "articles": []}

        all_data = []

        # Filter URLs by date range
        for data in urls_data:
            article_url = data['URL']
            article_date = format_date(data['Date'])

            if article_date and start_date <= article_date <= end_date:
                print(f"Processing URL: {article_url} (Date: {article_date})")
                content = extract_content_from_article(article_url)
                if content:
                    all_data.append({'Content': content})
                time.sleep(3)  # Add a delay between requests

        if all_data:
            print(f"Successfully scraped {len(all_data)} articles.")
            # driver.quit()
            return all_data
        
        else:
            print("No valid data found within the specified date range.")
            return {"message": "unsuccessful", "articles": []}

    except Exception as e:
        print(f"Error processing URL: error")
        return { []}

    finally:
        print('completes')
        # driver.quit()

# Example usage
# response = scrape_url_web3('https://totalenergies.com.br/blog', '2024-07-01', '2024-10-18')
# print(response)
