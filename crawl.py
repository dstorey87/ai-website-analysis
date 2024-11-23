import sqlite3

import re

from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager


    chrome_options = Options()

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        trending_elements = driver.find_elements(By.CSS_SELECTOR, ".trend-card .trend-card__list a")

        trending_topics = [element.text for element in trending_elements]

    conn = sqlite3.connect(database_path)

    cursor = conn.cursor()

    match = re.match(r"crawl\s+(https?://[^\s]+)\s+for\s+(.+?),\s+store\s+(.+)", command, re.IGNORECASE)

    url, context, database_path = match.groups()

        trending_data = fetch_trending_data(url)

    conn = sqlite3.connect(database_path)

    cursor = conn.cursor()

    rows = cursor.fetchall()




def fetch_trending_data(url):
    """Fetch trending data from the given URL."""
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        driver.get(url)

        # Locate and extract trending topics (adjust selectors as needed)
        print("Fetched Topics:", trending_topics)  # Debugging: Print fetched topics
        return trending_topics
    finally:
        driver.quit()


def save_to_database(database_path, data):
    """Save the extracted data to a SQLite database."""
    print(f"Data to Save: {data}")  # Debugging: Print data before saving
    if not data:
        print("No data to save. Exiting function.")
        return  # Exit if there's no data to save


    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    try:
        # Insert data
        cursor.executemany("INSERT INTO trends (topic) VALUES (?);", [(topic,) for topic in data])
        conn.commit()
        print("Data saved successfully.")  # Debugging: Confirm save
    except Exception as e:
        print(f"Error saving data to database: {e}")  # Debugging: Print any errors
    finally:
        conn.close()


def crawl_command_handler(command):
    """Parse the command and handle the crawling and storage."""
    # Parse the command
    if not match:
        raise ValueError("Invalid command format. Use: crawl <website> <context> <database>")


    # Fetch data based on the context
    if "trending data" in context.lower():
        print(f"Fetching trending data from {url}...")
        print("Data fetched successfully.")

        # Save only website data to database
        save_to_database(database_path, trending_data)
        print(f"Data saved to database: {database_path}")

        # Return a summary for display
        return trending_data

    else:
        raise ValueError(f"Context '{context}' is not supported.")


def retrieve_from_database(database_path):
    """Retrieve data from the SQLite database."""

    # Query all data from the trends table
    cursor.execute("SELECT topic FROM trends ORDER BY timestamp DESC;")

    conn.close()

    # Return only the topics
    return [row[0] for row in rows]
