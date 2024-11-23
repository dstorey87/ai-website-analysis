import sqlite3

DB_PATH = "trends24.db"

def retrieve_trends():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT topic, url, timestamp FROM trending_topics
    ORDER BY timestamp DESC
    LIMIT 50
    """)
    rows = cursor.fetchall()
    conn.close()
    
    return rows

if __name__ == "__main__":
    trends = retrieve_trends()
    for topic, url, timestamp in trends:
        print(f"{timestamp}: {topic} - {url}")
