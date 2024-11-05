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
chrome_options.add_argument("--headless")  # Uncomment to run headless
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--log-level=3") 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def accept_cookies():
    """Click the accept cookies button if it appears."""
    try:
        # Wait for the button to be present and clickable
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        button.click()
        print("Cookies accepted.")
    except Exception as e:
        print("No cookie consent button found or couldn't click it:", e)

def extract_article_info_from_page(url, start_date, end_date):
    """Extracts and filters article links and dates from the specified URL based on date range."""
    try:
        driver.get(url)
        accept_cookies()  # Call the function to accept cookies

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article.c.c-d.c--m'))
        )

        articles = driver.find_elements(By.CSS_SELECTOR, 'article.c.c-d.c--m')
        extracted_info = []

        for article in articles:
            try:
                link_element = article.find_element(By.CSS_SELECTOR, 'header.c_h h2 a')
                date_element = article.find_element(By.CSS_SELECTOR, 'div.c_a time')

                article_link = link_element.get_attribute('href')
                article_date_str = date_element.get_attribute('datetime')
                article_date = datetime.fromisoformat(article_date_str).date() if article_date_str else None

                if article_link and article_date and start_date <= article_date <= end_date:
                    extracted_info.append({'URL': article_link, 'Date': article_date})
                    print(f"Extracted URL: {article_link}, Date: {article_date}")
            except Exception as e:
                print(f"Error extracting information from article: {e}")

        return extracted_info

    except Exception as e:
        print(f"Error loading page {url}: {e}")
        return []

def extract_full_article_content(url):
    """Extracts the full article content from the specified URL, including headline, subheadline, and paragraphs."""
    try:
        driver.get(url)
        # Wait for the article content to be present within a timeout
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.a_c.clearfix p'))
        )
        
        # Extract headline, subheadline, and content
        paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div.a_c.clearfix p')
        content = '\n'.join(p.text for p in paragraphs)

        return {'Content': content}

    except Exception as e:
        print(f"Error extracting article content from {url}: {e}")
        return {'Content': ''}

def scrape_url_web4(url, start_date_str, end_date_str):
    """Function that extracts article info from the specified URL, filters by date, and returns article content."""
    try:
        # Convert start_date_str and end_date_str to datetime.date objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        print(f"Processing URL: {url}")
        time.sleep(4)  # You may want to adjust this if necessary
        article_info = extract_article_info_from_page(url, start_date, end_date)

        all_data = []
        for info in article_info:
            content = extract_full_article_content(info['URL'])
            if content['Content']:
                all_data.append({'Content': content['Content']})
                print(f"Extracted content for URL: {info['URL']}")

            time.sleep(2)  # Be courteous and avoid overloading the server

        if all_data:
            # Return the success message and the extracted articles
            return all_data
        else:
            print("No valid data found within the specified date range.")
            return []

    except Exception as e:
        print(f"Error processing the URL: {e}")
        return {"message": "unsuccessful", "articles": []}

# Example usage
# response = scrape_url_web4('https://english.elpais.com/usa/', '2024-05-01', '2024-10-24')
# print(response)

# Close the driver at the end
# driver.quit()
