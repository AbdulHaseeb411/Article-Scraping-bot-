from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from dateutil import parser
from datetime import timezone

# Set up the Selenium WebDriver with Chrome options
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # Uncomment this if you want to run in headless mode
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")  # Minimize Chrome's internal logs
chrome_options.add_argument("--enable-unsafe-swiftshader")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def is_date_in_range(article_date, start_date, end_date):
    """Check if the article date is within the specified range."""
    print("Checking", article_date, start_date, end_date)
    return start_date <= article_date <= end_date

def extract_links_and_dates(url, start_date, end_date):
    """Extracts article links and dates from the specified URL and filters them based on the date range."""
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article.newscard-default'))
        )

        articles = driver.find_elements(By.CSS_SELECTOR, 'article.newscard-default')
        filtered_articles = []

        for article in articles:
            try:
                link_element = article.find_element(By.CSS_SELECTOR, 'h2 a')
                date_element = article.find_element(By.CSS_SELECTOR, 'time')

                article_link = link_element.get_attribute('href')
                date_str = date_element.get_attribute('datetime')  # or date_element.text based on the actual structure
                
                # Parse the date
                article_date = parser.isoparse(date_str)

                # Print the URL and the parsed date for debugging
                print(f"URL: {article_link}, Parsed Date: {article_date}")

                # Filter by date range
                if article_link and article_date and is_date_in_range(article_date, start_date, end_date):
                    print(f"Article in range: {article_link} | Date: {article_date}")
                    filtered_articles.append({
                        'URL': article_link,
                        'Date': article_date
                    })

            except Exception as e:
                print(f"Error processing article: error")
                continue  # Skip to the next article if there is an error

        return filtered_articles

    except Exception as e:
        print(f"Error extracting articles: error")
        return []

def scrape_article_content(article_url):
    """Scrapes the content of the article from the provided URL."""
    try:
        driver.get(article_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
        )

        # Extract header
        header = None
        try:
            header_element = driver.find_element(By.CSS_SELECTOR, 'h1')
            header = header_element.text
        except Exception:
            header = "Header not found"

        # Extract content
        content = []
        try:
            content_elements = driver.find_elements(By.CSS_SELECTOR, 'div.entry-content.overflow-hidden p')
            content = [p.text for p in content_elements]
        except Exception:
            content = []

        # Combine header and content
        combined_content = header + ' ' + ' '.join(content) if header else ' '.join(content)

        return combined_content

    except Exception as e:
        print(f"Error scraping article content: error")
        return None

def scrape_url_web5(url, start_date_str, end_date_str):
    """Extracts articles from the specified URL, filters them by date range, and scrapes the content of the filtered articles."""
    try:
        # Convert start_date_str and end_date_str to datetime objects
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        # Step 1: Extract and filter article links and dates
        filtered_articles = extract_links_and_dates(url, start_date, end_date)

        if not filtered_articles:
            return {"message": "unsuccessful", "articles": []}

        # Step 2: Scrape content for each filtered article
        article_info = []
        for article in filtered_articles:
            print(f"Scraping content for article: {article['URL']}")
            combined_content = scrape_article_content(article['URL'])

            if combined_content:
                article_info.append({
                   
                    'CombinedContent': combined_content
                })

        return  article_info

    except Exception as e:
        print(f"Error in scraping: error")
        return {"message": "unsuccessful", "articles": []}

# Example usage
# response = scrape_url_web5('https://infomercado.pe/ultimas-noticias/', '2024-10-01', '2024-10-16')
# print(response)

# Close the driver after use
# driver.quit()
