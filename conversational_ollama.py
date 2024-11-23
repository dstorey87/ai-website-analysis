import sqlite3

import subprocess

import sys

import io

from website_analyzer import crawl_command_handler, retrieve_from_database


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")

DATABASE_PATH = "C:\\sqlite\\llama_conversations.db"

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    result = cursor.fetchone()

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    WHERE conversation_id = ? 

    rows = cursor.fetchall()

    context = "\n".join([f"{role}: {content}" for role, content in rows])

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

        process = subprocess.run(

            capture_output=True,

            text=True,

            encoding="utf-8",  # Explicitly set encoding to UTF-8

            check=True

    last_conversation_id = get_last_conversation_id()

        context = get_conversation_context(last_conversation_id)

        context = ""

        last_conversation_id = 0

    conversation_id = last_conversation_id + 1

    turn_id = 1

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":

        elif user_input.lower() == "clear":

            context = ""

        elif user_input.lower() == "review":

            previous_context = get_conversation_context(last_conversation_id)

                extracted_data = crawl_command_handler(user_input)

                analysis_result = "Data crawled:\n" + "\n".join(extracted_data)

                context += f"\nWebsite Analysis:\n{analysis_result}"

                model_response = interact_with_ollama(context)

                    turn_id += 1

                database_path = user_input.split(" ")[1]

                retrieved_data = retrieve_from_database(database_path)

                analysis_result = "Retrieved Data:\n" + "\n".join(retrieved_data)

                context += f"\nRetrieved Data:\n{analysis_result}"

            context += f"\nUser: {user_input}"

            model_response = interact_with_ollama(context)

                context += f"\nLlama 3.2 Vision: {model_response}"

                turn_id += 1

        turn_id += 1

if __name__ == "__main__":




# Path to your SQLite database

# Function to initialize the database
def initialize_database():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        conversation_id INTEGER NOT NULL,
        turn_id INTEGER NOT NULL,
        role TEXT NOT NULL, -- 'user' or 'model'
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (conversation_id, turn_id)
    );
    """)
    conn.commit()
    conn.close()

# Function to retrieve the last conversation ID
def get_last_conversation_id():
    cursor.execute("SELECT MAX(conversation_id) FROM conversations")
    conn.close()
    return result[0] if result[0] is not None else 0

# Function to retrieve the full context of a conversation
def get_conversation_context(conversation_id):
    cursor.execute("""
    SELECT role, content 
    FROM conversations 
    ORDER BY turn_id
    """, (conversation_id,))
    conn.close()

    # Format the conversation context as a single string
    return context

# Function to insert a message into the database
def insert_message(conversation_id, turn_id, role, content):
    cursor.execute(
        "INSERT INTO conversations (conversation_id, turn_id, role, content) VALUES (?, ?, ?, ?)",
        (conversation_id, turn_id, role, content)
    )
    conn.commit()
    conn.close()

# Function to interact with Ollama
def interact_with_ollama(context):
    try:
            ["ollama", "run", "llama3.2-vision", context],
        )
        return process.stdout.strip()  # Response from the model
    except subprocess.CalledProcessError as e:
        print(f"Error interacting with Ollama: {e}")
        return None

# Function to handle a conversation
def conversation_loop():
    initialize_database()
    
    if last_conversation_id > 0:
        print("Previous conversation detected. Loading context...")
    else:
        print("No previous conversation found. Starting a new one.")


    print("Start your conversation with Llama 3.2 Vision. Type 'exit' to end.")
    while True:
        # Show context for reference
        if context:
            print("\nConversation so far:")
            print(context)
            print()

        # User input
            print("Conversation ended.")
            break

            # Clear the conversation context
            print("Conversation context cleared. You can still review previous conversations with 'review'.")

            # Reload the previous conversation context
            print("Reviewing previous conversations...")
            if previous_context:
                print("Previous Conversation:")
                print(previous_context)
            else:
                print("No previous conversation found.")

        elif user_input.lower().startswith("crawl"):
            try:
                # Execute the crawl command
                print("Processing crawl command...")
                
                # Prepare the result for display

                # Append only the result summary to context for reference
                
                # Send result to Llama 3.2 Vision
                if model_response:
                    print(f"Llama 3.2 Vision: {model_response}")

                    # Save model response to the conversation database
                    insert_message(conversation_id, turn_id, "model", model_response)

            except Exception as e:
                print(f"Error processing crawl command: {e}")
                continue

        elif user_input.lower().startswith("retrieve"):
            try:
                # Parse the database name from the command
                print(f"Retrieving data from {database_path}...")

                # Fetch only the website data

                if not retrieved_data:
                    print("No data found in the database.")
                    continue

                # Display only the retrieved data
                print(analysis_result)

                # Optionally append only the retrieved data summary to context

            except Exception as e:
                print(f"Error retrieving data: {e}")
                continue

        else:
            # Append user input to context

            # Save user input to the database
            insert_message(conversation_id, turn_id, "user", user_input)

            # Get model response with full context
            if model_response:
                print(f"Llama 3.2 Vision: {model_response}")

                # Append model response to context

                # Save model response to the database
                insert_message(conversation_id, turn_id, "model", model_response)

        # Increment turn_id for the next user input

    conversation_loop()
