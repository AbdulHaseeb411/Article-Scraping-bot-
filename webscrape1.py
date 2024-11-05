from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import csv

# Configure the Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run headless for no GUI
chrome_options.add_argument("--log-level=3") 
# Set up the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to check if the date is within the range
def is_date_in_range(news_date, start_date, end_date):
    # Adjust the format to match 'Publicado em DD/MM/YYYY'
    news_date = datetime.strptime(news_date, "Publicado em %d/%m/%Y")
    return start_date <= news_date <= end_date

# Main scraping function
def scrape_url_web1(url, start_date_input, end_date_input):
    try:
        # Parse input dates in 'YYYY-MM-DD' format
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_input, "%Y-%m-%d")

        # List of category IDs to check
        category_ids = ["10629433", "10629482"]

        # Open the current URL
        print('runing===================',url)
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Find all elements with class name "card-news"
        news_elements = driver.find_elements(By.CSS_SELECTOR, ".card")

        # Prepare a list to store the filtered articles
        news_data = []

        # Iterate over the found elements and extract the necessary data
        for element in news_elements:
            category_id = element.get_attribute("category-id")

            # Check if the category_id is in the list of desired category IDs
            if category_id in category_ids:
                try:
                    # Get the URL of the news article
                    title_element = element.find_element(By.CSS_SELECTOR, ".editorial-news-card-link")
                    news_url = title_element.get_attribute("href")
                    
                    # Get the date of the article
                    date_element = element.find_element(By.CSS_SELECTOR, ".updated")
                    news_date = date_element.text

                    # Check if the date is within the specified range
                    if is_date_in_range(news_date, start_date, end_date):
                        # Store the data if the date matches the range
                        news_data.append({
                            "url": news_url,
                            "date": news_date
                        })
                except Exception as e:
                    print(f"Error processing element: error")

        # Collecting contents of filtered articles
        results = []
        for news in news_data:
            news_url = news["url"]
            # Open the news article URL
            driver.get(news_url)
            time.sleep(3)  # Wait for the page to load

            try:
                # Locate the div with class 'news-content breakpoint'
                news_content = driver.find_element(By.CSS_SELECTOR, ".news-content.breakpoint")
                
                # Find all <p> tags within that div
                paragraphs = news_content.find_elements(By.TAG_NAME, "p")
                
                # Concatenate all paragraphs into a single string
                content = "\n".join([paragraph.text for paragraph in paragraphs])
                
                results.append({
                    'URL': news_url,
                    'Date': news['date'],
                    'Content': content
                })
                print(f"Successfully scraped content from {news_url}.")
            except Exception as e:
                print(f"Error scraping content from {news_url}: error")
        
        # Return message based on the results
        if results:
            return  results
        else:
            return "No articles found in the specified date range", []

    finally:
        # Ensure that the driver is closed after scraping
        print('completes')
        # driver.quit()
# Example usage
# url = "https://agencia.petrobras.com.br/sustentabilidade"  # Replace with your URL
# start_date_input = "2024-07-10"  # In 'YYYY-MM-DD' format
# end_date_input = "2024-07-26"  # In 'YYYY-MM-DD' format

# message, articles = scrape_url_web1(url, start_date_input, end_date_input)

# print(message)
# for article in articles:
#     print(article)

# Close the browser

