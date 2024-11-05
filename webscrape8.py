import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import pandas as pd  # Import pandas for handling Excel files

# Set up ChromeDriver using webdriver_manager
def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--disable-software-rasterizer")  # Disable software rendering fallback
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")  # Minimize Chrome's internal logs
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
    chrome_options.add_argument("--disable-css")  # Disable CSS loading
    chrome_options.add_argument("--disable-javascript")  # Disable JS loading (if not needed)
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to extract article URLs and publication dates
def extract_articles_info(driver, url):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    extracted_data = []
    
    try:
        articles = driver.find_elements(By.CSS_SELECTOR, "article.et_pb_post")
        
        for article in articles:
            try:
                article_url = article.find_element(By.CSS_SELECTOR, "h2.entry-title a").get_attribute("href")
                publication_date = article.find_element(By.CSS_SELECTOR, "span.published").text
                
                if publication_date:
                    publication_date = convert_date(publication_date)
                    print(f"Extracted: {article_url}, Date: {publication_date}")
                    extracted_data.append([article_url, publication_date])
                else:
                    print(f"Skipped {article_url} due to empty publication date.")
            except Exception as e:
                print(f"Error extracting data from article: error")
                continue
        
        return extracted_data
    except Exception as e:
        print(f"Error extracting data from {url}: error")
        return []

# Function to translate Spanish month names to English
def translate_month(spanish_month):
    months = {
        "enero": "January",
        "febrero": "February",
        "marzo": "March",
        "abril": "April",
        "mayo": "May",
        "junio": "June",
        "julio": "July",
        "agosto": "August",
        "septiembre": "September",
        "octubre": "October",
        "noviembre": "November",
        "diciembre": "December"
    }
    return months.get(spanish_month.lower(), None)

# Function to convert publication date to a standard format
def convert_date(date_str):
    try:
        if any(month in date_str.lower() for month in ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]):
            month_str = date_str.split(" ")[0]
            month = translate_month(month_str)
            if month:
                day = date_str.split(" ")[1].strip(',')
                year = date_str.split(" ")[2]
                date = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
                return date.strftime("%Y-%m-%d")
        else:
            date = datetime.strptime(date_str, "%b %d, %Y")
            return date.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error converting date '{date_str}':")
        return date_str

# Function to filter extracted articles by date
def filter_by_date(extracted_data, start_date, end_date):
    filtered_data = []
    for url, pub_date in extracted_data:
        pub_date_obj = datetime.strptime(pub_date, "%Y-%m-%d")
        if start_date <= pub_date_obj <= end_date:
            filtered_data.append([url, pub_date])
    return filtered_data

# Function to extract content from the article page
def extract_content(driver, url):
    driver.get(url)
    time.sleep(6)  # Wait for the page to load
    
    try:
        content_element = driver.find_element(By.ID, "single-content")
        paragraphs = content_element.find_elements(By.TAG_NAME, "p")
        content = "\n".join([p.text for p in paragraphs if p.text])  # Join text from each <p> tag
        return content
    except Exception as e:
        print(f"Error extracting content from {url}: ")
        return ""

# Function to scrape articles based on input parameters
def scrape_url_web8(input_url, start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Setup the Selenium driver
    driver = setup_driver()

    extracted_data = extract_articles_info(driver, input_url)

    filtered_data = filter_by_date(extracted_data, start_date, end_date)

    if filtered_data:
        content_data = []
        for url, pub_date in filtered_data:
            content = extract_content(driver, url)
            content_data.append({"Content":content})  # Append each row to the list
        print(content_data)
        print("Scraping successful! Filtered articles:")
        # for row in content_data:
        #     # print(f"Content: {row[2]}")  # Print first 100 characters of content
        #     # print('content=======================',content)
        return content_data
    else:
        print("No articles found within the specified date range.")
        return "Unsuccessful", []


   
result = scrape_url_web8('https://www.mch.cl/categoria/negocios-industria/comunidades/', '2024-09-25', '2024-10-08')
print(result)
