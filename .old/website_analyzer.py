import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def fetch_trending_data(url):
    """Fetch trending data from the given URL."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        driver.get(url)

        # Locate and extract trending topics (adjust selectors as needed)
        trending_elements = driver.find_elements(By.CSS_SELECTOR, ".trend-card .trend-card__list a")
        trending_topics = [element.text for element in trending_elements]

        return trending_topics
    finally:
        driver.quit()

def save_to_database(database_path, data):
    """Save the extracted data to a SQLite database."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trends (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Insert data
    cursor.executemany("INSERT INTO trends (topic) VALUES (?);", [(topic,) for topic in data])

    conn.commit()
    conn.close()

def crawl_command_handler(command):
    """Parse the command and handle the crawling and storage."""
    import re

    # Parse the command
    match = re.match(r"crawl\s+(https?://[^\s]+)\s+for\s+(.+?),\s+store\s+(.+)", command, re.IGNORECASE)
    if not match:
        raise ValueError("Invalid command format. Use: crawl <website> <context> <database>")

    url, context, database_path = match.groups()

    # Fetch data based on the context
    if "trending data" in context.lower():
        print(f"Fetching trending data from {url}...")
        trending_data = fetch_trending_data(url)
        print("Data fetched successfully.")

        # Save to database
        save_to_database(database_path, trending_data)
        print(f"Data saved to database: {database_path}")

        return trending_data

    else:
        raise ValueError(f"Context '{context}' is not supported.")

def retrieve_from_database(database_path):
    """Retrieve data from the SQLite database."""
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Query all data
    cursor.execute("SELECT topic FROM trends ORDER BY timestamp DESC;")
    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]
