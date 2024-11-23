import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurations
TRENDS24_URL = "https://trends24.in/"
DB_PATH = "trends24.db"

# Function to set up the browser
def setup_browser():
    """
    Sets up the Selenium WebDriver with ChromeDriver.
    Returns:
        WebDriver: An instance of Selenium WebDriver.
    """
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for automation
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    try:
        print("Setting up ChromeDriver...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("ChromeDriver setup successful.")
    except Exception as e:
        print(f"Error during ChromeDriver setup: {e}")
        raise
    return driver

# Function to fetch trending topics
def fetch_trending_topics():
    """
    Fetch trending topics from Trends24 using Selenium.
    Returns:
        list: A list of tuples containing topic text and URLs.
    """
    trends = []
    driver = setup_browser()
    try:
        print("Opening Trends24...")
        driver.get(TRENDS24_URL)
        time.sleep(3)  # Allow the page to load
        print("Scraping trending topics...")
        topics = driver.find_elements(By.CSS_SELECTOR, "li a")
        trends = [(topic.text, topic.get_attribute("href")) for topic in topics if topic.text]
        print(f"Found {len(trends)} topics.")
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()
        print("Browser closed.")
    return trends

# Function to save trends to the database
def save_to_database(trends):
    """
    Saves fetched trends into the SQLite database.
    Args:
        trends (list): A list of tuples containing topic text and URLs.
    """
    if not trends:
        print("No trends to save.")
        return
    print("Saving trends to the database...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trending_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            url TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # Insert data
        cursor.executemany("""
        INSERT INTO trending_topics (topic, url) VALUES (?, ?)
        """, trends)
        conn.commit()
        print("Trends saved successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# Main function to coordinate scraping and saving
def main():
    try:
        print("Starting the scraper...")
        trends = fetch_trending_topics()
        save_to_database(trends)
        print("Scraper completed successfully.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the script
if __name__ == "__main__":
    main()
