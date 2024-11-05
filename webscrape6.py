import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def scrape_article_urls(url):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument("--log-level=3") 
    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    article_links = []

    try:
        print(f"Scraping article URLs from {url}...")
        driver.get(url)

        # Locate the elements containing articles
       
        articles = driver.find_elements(By.CSS_SELECTOR, ".view-content .grid.list-group-item")
        print(f"Found {len(articles)} articles.")

        for article in articles:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, ".views-field-title a")
                link = title_element.get_attribute("href")
                article_links.append(link)

            except Exception as e:
                print(f"Error getting article link: {e}")

        print("Article URLs scraping complete.")
        return article_links

    except Exception as e:
        print(f"An error occurred while scraping {url}: {e}")
        return []

    finally:
        print('completes url')
        # driver.quit()

def scrape_article_content(link):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")  # Uncomment if running without a GUI
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")  # Minimize Chrome's internal logs
    chrome_options.add_argument("--enable-unsafe-swiftshader")
    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    content = ""

    try:
        print(f"Scraping content from article: {link}")
        driver.get(link)

        # # Wait for the article page to load and click "Leer Más"
        # try:
        #     time.sleep(3)
        #     read_more_button = WebDriverWait(driver, 15).until(
        #         EC.element_to_be_clickable((By.CLASS_NAME, "a.tbl-read-more-btn"))
        #     )
        #     read_more_button.click()
        #     print("Clicked on 'Leer Más' button.")
        # except Exception as e:
        #     print("Could not click 'Leer Más' button:", )

        # Wait for the content to load
        time.sleep(5)

        # Scrape the content
        
        content_div = driver.find_element(By.CSS_SELECTOR, "div[property='schema:text']")
        paragraphs = content_div.find_elements(By.TAG_NAME, 'p')
        content = ' '.join([p.text for p in paragraphs])  # Join paragraphs into a single string

        print(f"Content: {content}")

    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    finally:
        print('completes')
        # driver.quit()

    return content  # Return only the content

def scrape_url_web6(url, start_date, end_date):
    article_links = scrape_article_urls(url)

    all_articles = []
    for link in article_links:
        article_content = scrape_article_content(link)  # Get plain content
        if article_content:  # Check if content was successfully scraped
            all_articles.append({'Content': article_content})  # Keep links if needed

    print('======================all_articles==================>>',all_articles)
    return all_articles

    # if not all_articles:
    #     # You can filter by your desired criteria if needed here
    #     print(f"Total articles scraped: {len(all_articles)}")
    #     return "Successful", all_articles  # Return the DataFrame

    # else:
    #     print("No articles to filter.")
    #     return "Unsuccessful", []

# Example usage
# url = "https://www.lapatria.com/manizales"
# start_date = "2024-10-25"  # Example start date
# end_date = "2024-10-26"    # Example end date

# status, articles_df = scrape_url_web6(url, start_date, end_date)
# if status == "Successful":
#     print("Scraped Articles:")
#     print(articles_df)
# else:
#     print("Failed to scrape articles.")
