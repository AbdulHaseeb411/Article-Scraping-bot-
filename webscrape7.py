import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Dictionary to convert Spanish month names to English
SPANISH_TO_ENGLISH_MONTHS = {
    'ENERO': 'January', 'FEBRERO': 'February', 'MARZO': 'March', 'ABRIL': 'April',
    'MAYO': 'May', 'JUNIO': 'June', 'JULIO': 'July', 'AGOSTO': 'August',
    'SEPTIEMBRE': 'September', 'OCTUBRE': 'October', 'NOVIEMBRE': 'November', 'DICIEMBRE': 'December'
}

# Function to convert Spanish date to an English date string
def convert_spanish_date_to_english(spanish_date_str):
    try:
        parts = spanish_date_str.split()
        month_in_english = SPANISH_TO_ENGLISH_MONTHS.get(parts[0].upper(), None)
        if month_in_english:
            english_date_str = f"{month_in_english} {parts[1].strip(',')}, {parts[2]}"
            return english_date_str
        else:
            print(f"Unknown month name in date: {spanish_date_str}")
            return None
    except Exception as e:
        print(f"Error converting date {spanish_date_str}: {e}")
        return None

# Function to extract content between <p> tags within the <article> tag
def extract_article_content(driver, article_url, retries=3):
    print(f"Opening article URL: {article_url}")
    for i in range(retries):
        try:
            driver.get(article_url)
            # Wait until the article element is present
            article_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))

            # Find all <p> tags within the article
            paragraphs = article_element.find_elements(By.TAG_NAME, "p")
            article_content = "\n".join(p.text for p in paragraphs)
            print(f"Extracted content from {article_url}")
            return article_content
        except Exception as e:
            print(f"Error extracting article content from {article_url}: {e}")
            if i < retries - 1:
                print(f"Retrying... ({i+1}/{retries})")
                time.sleep(3)  # Delay before retrying
            else:
                return ""

# Function to extract article URLs and their dates
def scrape_article_urls_and_dates(driver, url, retries=3):
    print(f"Scraping main page: {url}")
    articles_data = []
    for i in range(retries):
        try:
            driver.get(url)
            # Wait for article elements to be present
            articles = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.article")))

            for article in articles:
                try:
                    article_url = article.find_element(By.CSS_SELECTOR, "div.title a").get_attribute("href")
                    date_element = article.find_element(By.CSS_SELECTOR, "div.meta time")
                    publication_date_text = date_element.text.upper()

                    english_date_str = convert_spanish_date_to_english(publication_date_text)
                    if english_date_str:
                        publication_date = datetime.strptime(english_date_str, "%B %d, %Y")
                        articles_data.append({
                            "URL": article_url,
                            "Date": publication_date
                        })
                        print(f"Found article: {article_url}, Date: {publication_date}")
                except Exception as e:
                    print(f"Error processing article in {url}: {e}")

            return articles_data  # Exit loop on success
        except Exception as e:
            print(f"Error scraping articles from {url}: {e}")
            if i < retries - 1:
                print(f"Retrying... ({i+1}/{retries})")
                time.sleep(3)  # Delay before retrying
            else:
                return articles_data

# Function to scrape, filter by date, and extract content from articles
def scrape_url_web7(url, start_date_str, end_date_str):
    # Set up Chrome options for headless mode and other optimizations
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--disable-software-rasterizer")  # Disable software rendering fallback
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")  # Minimize Chrome's internal logs
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
    chrome_options.add_argument("--disable-css")  # Disable CSS loading
    chrome_options.add_argument("--disable-javascript")  # Disable JS loading (if not needed)
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    
    # Start Chrome driver in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    refined_articles = []

    try:
        articles_data = scrape_article_urls_and_dates(driver, url)
        
        # Filter articles by date and extract content concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(extract_article_content, driver, article["URL"]): article for article in articles_data if start_date <= article["Date"] <= end_date}
            for future in concurrent.futures.as_completed(future_to_url):
                article = future_to_url[future]
                try:
                    article_content = future.result()
                    refined_articles.append({
                       
                        "Content": article_content
                    })
                except Exception as e:
                    print(f"Error extracting content from {article['URL']}: {e}")

        # Return success message and the scraped articles
        if refined_articles:
            print("Scraping successful.")
            return refined_articles
        else:
            print("No articles found within the date range.")
            return "No articles found within the date range.", []

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return f"Scraping unsuccessful due to an error: {e}", []

    finally:
        print('completes')
        # driver.quit()

# Example of how to use the function
# url = 'https://www.elnacional.com/politica/'
# start_date = '2024-10-01'
# end_date = '2024-10-30'

# message, articles = scrape_url_web7(url, start_date, end_date)
# print(message)
# for article in articles:
#     print(article)
