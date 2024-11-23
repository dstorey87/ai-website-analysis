import sqlite3

DB_PATH = "C:\\AI_Content_App\\Datavbase_conf\\trends24.db"

def check_table_exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='trending_topics';
    """)
    table_exists = cursor.fetchone() is not None
    conn.close()
    return table_exists

if __name__ == "__main__":
    if check_table_exists():
        print("Table 'trending_topics' exists.")
    else:
        print("Table 'trending_topics' does not exist.")
