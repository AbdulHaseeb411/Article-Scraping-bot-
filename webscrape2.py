import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from datetime import datetime

# Setup Chrome options
chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3") 
# chrome_options.add_argument("--headless") 
# Set up the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Portuguese to English month name mapping
month_translation = {
    'janeiro': 'January',
    'fevereiro': 'February',
    'março': 'March',
    'abril': 'April',
    'maio': 'May',
    'junho': 'June',
    'julho': 'July',
    'agosto': 'August',
    'setembro': 'September',
    'outubro': 'October',
    'novembro': 'November',
    'dezembro': 'December'
}

def convert_portuguese_date(date_text):
    for pt_month, en_month in month_translation.items():
        if pt_month in date_text.lower():
            return date_text.lower().replace(pt_month, en_month).title()
    return date_text

def scrape_data(url, start_date, end_date):
    driver.get(url)
    time.sleep(3)

    items = driver.find_elements(By.CSS_SELECTOR, '.item')

    data = []
    for item in items:
        try:
            # Extract the date
            date_elem = item.find_element(By.CSS_SELECTOR, '.data')
            date_text = date_elem.find_element(By.TAG_NAME, 'b').text.strip() + " " + date_elem.text.strip().replace(date_elem.find_element(By.TAG_NAME, 'b').text.strip(), '').strip()
            
            date_text = convert_portuguese_date(date_text)
            
            # Parse the date
            try:
                item_date = datetime.strptime(date_text, '%d de %B de %Y')
            except ValueError:
                try:
                    item_date = datetime.strptime(date_text, '%d %B')
                    item_date = item_date.replace(year=datetime.now().year)
                except ValueError:
                    print(f"Date format '{date_text}' not recognized.")
                    continue

            # Check if the item date is within the specified range
            if start_date <= item_date <= end_date:
                # Extract the title and link
                title_element = item.find_element(By.CSS_SELECTOR, '.conteudo h2 a')
                title = title_element.text.strip()
                link = title_element.get_attribute('href')
                
                # Extract the description
                description = item.find_element(By.CSS_SELECTOR, '.conteudo p').text.strip()

                data.append({
                    'date': date_text,
                    'title': title,
                    'link': link,
                    'description': description
                })
            # driver.quit()
        except Exception as e:
            print(f"Error extracting data from an item:")

    return data

def scrape_content(url):
    driver.get(url)
    time.sleep(3)

    try:
        # Extract the title
        title = driver.find_element(By.CSS_SELECTOR, 'h2').text.strip()
        # Extract the date
        date_text = driver.find_element(By.CSS_SELECTOR, '.data').text.strip()
        date_text = convert_portuguese_date(date_text)
        
        # Parse the date
        try:
            item_date = datetime.strptime(date_text, '%d de %B de %Y')
        except ValueError:
            try:
                item_date = datetime.strptime(date_text, '%d %B')
                item_date = item_date.replace(year=datetime.now().year)
            except ValueError:
                print(f"Date format '{date_text}' not recognized.")
                return None

        # Extract the content
        content_elements = driver.find_elements(By.CSS_SELECTOR, '.content p')
        content = ' '.join([p.text.strip() for p in content_elements])

        return {
            'date': date_text,
            'title': title,
            'content': content
        }
    except Exception as e:
        print(f"Error extracting data from URL {url}: error")
        return None

def scrape_url_web2(url, start_date_str, end_date_str):
    try:
        # Convert input dates from 'YYYY-MM-DD' to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Scrape data from the given URL
        print(f"Scraping URL: {url}")
        data = scrape_data(url, start_date, end_date)

        if not data:
            print("No data found within the date range.")
            return {
                "message": "unsuccessful",
                "articles": []
            }
        
        all_articles = []
        for item in data:
            content_data = scrape_content(item['link'])
            if content_data:
                all_articles.append(content_data)

        # If articles were successfully retrieved
        if all_articles:
            
            print(f"Successfully scraped {len(all_articles)} articles.")
            return {
                all_articles
            }
        else:
            print("No articles matched the criteria.")
            return {
                "message": "unsuccessful",
                "articles": []
            }

    except Exception as e:
        print(f"An error occurred: error")
        return {
            
             []
        }

    finally:
        print('completes')
        # driver.quit()

# Example Usage:
# url = "https://eneva.com.br/sala-de-imprensa/noticias/?cat=83"  # Replace with the actual URL
# start_date = "2024-09-01"  # Example start date in 'YYYY-MM-DD' format
# end_date = "2024-10-18"    # Example end date in 'YYYY-MM-DD' format

# # # Call scrape_url to get the response
# response = scrape_url_web2(url, start_date, end_date)
# print(response)
