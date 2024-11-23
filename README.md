
# AI-Driven Website Analysis Chat Application

This application enables users to interact with a conversational AI model, analyze websites for trending data, and store meaningful insights into a persistent database. It combines web crawling, data storage, and natural language interaction for a seamless experience.

---

## Features

1. **Two-Way Conversation**:
   - Continuously interactive chat interface powered by Llama 3.2 Vision.
   - Persistent memory for storing and revisiting conversations.

2. **Website Crawling**:
   - Fetch and store trending topics from websites like `trends24.in`.
   - Extract meaningful data and save it to an SQLite database (`crawl.db`).

3. **Data Persistence**:
   - Store and retrieve conversations and crawled data using SQLite databases (`llama_conversations.db` and `crawl.db`).

4. **Commands**:
   - **`crawl`**: Crawl a website for specified data.
   - **`retrieve`**: Retrieve stored data from the database.
   - **`clear`**: Reset the current conversation context.
   - **`review`**: Reload previous conversations.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo-name/ai-website-analysis.git
   cd ai-website-analysis
   ```

2. **Install Dependencies**:
   Use Python 3.8+ and install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up SQLite Databases**:
   Initialize the required databases by running:
   ```bash
   python setup_databases.py
   ```

4. **Run the Application**:
   Start the chat interface:
   ```bash
   python conversational_ollama.py
   ```

---

## File Structure

```
Project/
├── crawl.py                 # Handles website crawling and database storage
├── setup_databases.py       # Sets up SQLite databases
├── conversational_ollama.py # Main conversational AI script
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

---

## Commands and Examples

### `crawl`
Fetch data from a website and store it in `crawl.db`.

Example:
```text
You: crawl http://trends24.in for all trending data, store crawl.db
Llama 3.2 Vision: Fetching trending data from http://trends24.in...
Data crawled:
- #Topic1
- #Topic2
- #Topic3
```

### `retrieve`
Retrieve stored data from the database.

Example:
```text
You: retrieve crawl.db
Llama 3.2 Vision: Retrieved Data:
- #Topic1
- #Topic2
- #Topic3
```

### `clear`
Clear the current conversation context without deleting stored data.

Example:
```text
You: clear
Llama 3.2 Vision: Conversation context cleared.
```

### `review`
Reload previous conversations.

Example:
```text
You: review
Llama 3.2 Vision: Previous Conversation:
User: Hello!
Llama 3.2 Vision: Hi there!
```

---

## How It Works

1. **Crawling Websites**:
   - The `crawl.py` script uses Selenium to scrape data from the specified URL.
   - Extracted data is saved into the `crawl.db` SQLite database.

2. **Conversation Management**:
   - The `conversational_ollama.py` script manages conversations and stores them in `llama_conversations.db`.

3. **Database Initialization**:
   - The `setup_databases.py` script sets up the required databases:
     - `llama_conversations.db`: Stores conversation history.
     - `crawl.db`: Stores website crawling data.

---

## Dependencies

- `selenium`: For web scraping.
- `sqlite3`: For database operations.
- `webdriver-manager`: To manage the browser driver.
- `ollama`: For interacting with the AI model.

Install them via:
```bash
pip install selenium sqlite3 webdriver-manager ollama
```

---

## Troubleshooting

1. **No Data After Crawling**:
   - Ensure the website's structure matches the CSS selectors in `crawl.py`.
   - Update the `trending_elements` selector if necessary.

2. **Database Issues**:
   - Verify database paths and permissions.
   - Ensure `setup_databases.py` was executed successfully.

3. **Model Not Responding**:
   - Confirm that the Ollama service is running.
   - Check subprocess communication for errors.

---

## Contributing

Feel free to open issues or submit pull requests to improve this project.

---

## License

This project is licensed under the MIT License.
