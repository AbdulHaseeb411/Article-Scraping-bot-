import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import random  # For adding random delays

# Function to parse the date from the article
def parse_date(date_str):
    try:
        if "Publicación:" in date_str:
            date_str = date_str.split(":")[1].strip()  # Keep only the relevant part
        
        date_str = date_str.strip()
        
        if "hace" in date_str.lower():  # Check for 'hace'
            parts = date_str.split()
            time_value = int(parts[1])
            
            if "minuto" in parts[2]:
                return datetime.now() - timedelta(minutes=time_value)
            elif "hora" in parts[2]:
                return datetime.now() - timedelta(hours=time_value)
            elif "día" in parts[2]:
                return datetime.now() - timedelta(days=time_value)
        
        elif "ayer" in date_str.lower():
            return datetime.now() - timedelta(days=1)
        
        else:
            # Try parsing as DD/MM/YYYY HH:MM
            try:
                return datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            except ValueError:
                print(f"Date format not recognized: {date_str}")
                return None
            
    except Exception as e:
        print(f"Error parsing date: {date_str}, Error: error")
        return None


# Function to extract article information
def extract_article_info(article):
    try:
        link = article.find_element(By.TAG_NAME, 'a').get_attribute('href')
        publication_date_elem = article.find_element(By.CSS_SELECTOR, '.publicationDate')
        publication_date_str = publication_date_elem.text.strip()

        print(f"Extracted URL: {link}, Publication Date String: {publication_date_str}")

        publication_date = parse_date(publication_date_str)
        
        return {
            'link': link,
            'date': publication_date,
        }
    except StaleElementReferenceException:
        print("Stale element reference encountered. Retrying extraction...")
        return None
    except NoSuchElementException:
        print("Error extracting info from article: No such element.")
        return None
    except Exception as e:
        print(f"Error extracting info from article: error")
        return None

# Function to extract paragraph text from a URL
def extract_paragraph_text(driver, url):
    try:
        driver.get(url)
        time.sleep(random.uniform(2, 4))  # Simulate real browsing behavior

        components = driver.find_elements(By.CSS_SELECTOR, '.articleComponent.text')
        all_paragraphs = []
        seen_texts = set()

        for component in components:
            paragraphs = component.find_elements(By.TAG_NAME, 'p')
            for paragraph in paragraphs:
                text = paragraph.text.strip()
                if text and text not in seen_texts:
                    all_paragraphs.append(text)
                    seen_texts.add(text)

        # Check other relevant elements (e.g., <h1>, <h2>, <span>)
        for component in components:
            for element in component.find_elements(By.XPATH, './/*[not(self::p)]'):
                text = element.text.strip()
                if text and text not in seen_texts:
                    all_paragraphs.append(text)
                    seen_texts.add(text)

        unique_paragraphs = list(dict.fromkeys(all_paragraphs))  # Keep order and remove duplicates

        article_text = "\n\n".join(unique_paragraphs)

        return article_text

    except Exception as e:
        print(f"Error extracting text from {url}: ")
        return None

    except Exception as e:
        print(f"Error extracting text from {url}: ")
        return None

# Function to process filtered URLs and extract paragraphs
def process_filtered_urls(driver, filtered_urls):
    paragraphs_content = []
    for url in filtered_urls:
        print(f"Processing URL: {url}")
        paragraph_text = extract_paragraph_text(driver, url)
        if paragraph_text:
            print(f"Extracted Paragraphs from {url}:")
            paragraphs_content.append(paragraph_text)
            print(paragraph_text)
        else:
            print(f"No paragraphs extracted from {url}.")
    return paragraphs_content

# Scraping function
def scrape_url_web9(url, start_date, end_date):
    start_date_str = start_date.strip() + " 00:00:00"
    end_date_str = end_date.strip() + " 23:59:59"  # End of the day

    print(start_date,end_date)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    options = Options()
    options.add_argument("--headless")  # Use headless mode if you do not need a UI
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--log-level=3") 
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        print(f"Opening URL: {url}")
        driver.get(url)

        articles = driver.find_elements(By.CSS_SELECTOR, 'article')
        print(f"Number of articles found: {len(articles)}")
        
        filtered_urls = []

        for article in articles:
            article_info = extract_article_info(article)
            if article_info and article_info['date']:
                print(start_date,article_info['date'],end_date)
                if start_date <= article_info['date'] <= end_date:
                    print(f"Filtered Article Link: {article_info['link']}, Date: {article_info['date']}")
                    filtered_urls.append(article_info['link'])
                else:
                    print("Article is not within the date range.")
            else:
                print("Article is not within the date range or missing data.")

        paragraphs_content = process_filtered_urls(driver, filtered_urls)

        if filtered_urls:
            print("Process completed successfully.")
            return paragraphs_content
        else:
            print("No articles found within the specified date range.")
            return "unsuccessful", []

    except TimeoutException:
        print("Page load timed out.")
        return "unsuccessful", []
    finally:
        print('completes')
        # driver.quit()

# # Example inputs
# url = "https://unitel.bo/noticias/seguridad"
# start_date ='2024-10-20 '  # Example start date
# end_date = '2024-10-24 '  # Example end date

# # Call the scrape function and print the message and filtered content
# message, filtered_content = scrape_url_web9(url, start_date, end_date)
# print(f"Message: {message}")
# print("Filtered Article Content:")
# for content in filtered_content:
#     print(content)
