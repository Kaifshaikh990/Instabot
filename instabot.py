import os
from instagrapi import Client
import random
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

if not USERNAME or not PASSWORD:
    print("ERROR: Missing Instagram credentials")

# Initialize the Instagram client
cl = Client()
try:
    cl.login(USERNAME, PASSWORD)
    print("Logged in successfully.")
except Exception as e:
    print(f"Error during login: {e}")
    exit(1)

# Function to process group messages
def process_group_message(message, thread_id):
    try:
        if "/percentages" in message.lower():
            percentage1 = random.randint(0, 100)
            percentage2 = random.randint(0, 100)
            response = f"Here are your random percentages:\n1. {percentage1}%\n2. {percentage2}%"
            cl.direct_send(response, thread_ids=[thread_id])
        elif "/help" in message.lower():
            response = "Available commands:\n/percentages - Get two random percentages\n/help - Show this message"
            cl.direct_send(response, thread_ids=[thread_id])
    except Exception as e:
        print(f"Error processing message: {e}")

# Main loop
try:
    while True:
        print("Checking for new messages in group chats...")
        threads = cl.direct_threads()

        for thread in threads:
            if thread.is_group:  # Only process group chats
                messages = cl.direct_messages(thread.id)
                for message in messages:
                    if not message.seen:  # Use 'message.seen' instead of 'seen_by_me'
                        print(f"New message in group {thread.title}: {message.text}")
                        process_group_message(message.text, thread.id)
                        cl.direct_mark_as_seen(thread.id)

        time.sleep(10)
except KeyboardInterrupt:
    print("Bot stopped.")
except Exception as e:
    print(f"Error: {e}")
