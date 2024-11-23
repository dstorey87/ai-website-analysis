import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Function to set up the browser with WebDriver Manager
from webdriver_manager.chrome import ChromeDriverManager

def setup_browser():
    """
    Sets up the Selenium WebDriver with WebDriver Manager.
    Returns:
        WebDriver: An instance of Selenium WebDriver.
    """
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for automation
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    try:
        print("Setting up ChromeDriver with WebDriver Manager...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("ChromeDriver setup successful.")
    except Exception as e:
        print(f"Error during ChromeDriver setup: {e}")
        raise
    return driver


# Function to scrape trends from Trends24
def fetch_trending_topics(url="https://trends24.in/"):
    """
    Fetches trending topics from Trends24 website.
    Args:
        url (str): The URL of Trends24.
    Returns:
        list: A list of tuples containing topic text and URLs.
    """
    driver = setup_browser()
    driver.get(url)
    time.sleep(3)  # Allow the page to load

    # Scrape trending topics
    try:
        topics = driver.find_elements(By.CSS_SELECTOR, "li a")
        trends = [(topic.text, topic.get_attribute("href")) for topic in topics if topic.text]
    except Exception as e:
        print(f"Error while scraping: {e}")
        trends = []
    finally:
        driver.quit()

    return trends


# Function to test scraping independently
if __name__ == "__main__":
    print("Fetching trends...")
    trends = fetch_trending_topics()
    for trend, link in trends:
        print(f"{trend}: {link}")
