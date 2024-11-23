from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from llama3_vision_llm import Llama3VisionLLM  # Ensure your custom Llama wrapper is properly set up
import time


def fetch_website_content(url):
    """Navigate to a website and extract content."""
    # Setup Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Automatically fetch and configure ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        time.sleep(2)  # Allow the page to load
        content = driver.find_element(By.TAG_NAME, "body").text  # Get the page's main text content
        return content
    except Exception as e:
        print(f"Error fetching website: {e}")
        return None
    finally:
        driver.quit()


class LlamaSession:
    """A session manager for persistent conversations with Llama."""
    def __init__(self):
        self.llama_llm = Llama3VisionLLM()  # Initialize the Llama model wrapper
        self.session_memory = []

    def add_to_session(self, user_input, response):
        """Add a user input and response to the session memory."""
        self.session_memory.append({"input": user_input, "response": response})

    def generate_prompt(self, content, user_input=None):
        """Generate a prompt for the Llama model."""
        context = "\n".join(
            [f"Input: {item['input']}\nResponse: {item['response']}" for item in self.session_memory]
        )
        if user_input:
            return f"Previous context:\n{context}\n\nNew input: {user_input}\n\nContent to analyze:\n{content}"
        return f"Content to analyze:\n{content}"

    def query_llama(self, content, user_input=None):
        """Query the Llama model with session context."""
        prompt = self.generate_prompt(content, user_input)
        response = self.llama_llm.invoke(prompt)
        if user_input:
            self.add_to_session(user_input, response)
        return response


if __name__ == "__main__":
    # Ask the user for the website URL
    website_url = input("Enter the website URL: ")

    # Step 1: Fetch website content
    print("Fetching website content...")
    content = fetch_website_content(website_url)

    if not content:
        print("Failed to fetch website content.")
    else:
        print(f"Fetched content (first 500 characters):\n{content[:500]}...\n")

        # Initialize the Llama session
        llama_session = LlamaSession()

        # Step 2: Analyze content with Llama
        print("Analyzing content with Llama 3.2 Vision...")
        initial_response = llama_session.query_llama(content)
        print("\nLlama 3.2 Vision Response:")
        print(initial_response)

        # Keep the session active for follow-up questions
        while True:
            follow_up = input("\nEnter a follow-up question (or type 'exit' to end): ")
            if follow_up.lower() == "exit":
                print("Session ended.")
                break

            # Query the Llama model with the follow-up
            follow_up_response = llama_session.query_llama(content, follow_up)
            print("\nLlama 3.2 Vision Follow-Up Response:")
            print(follow_up_response)
