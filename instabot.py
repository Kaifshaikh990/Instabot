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

# Maintain a list of processed message IDs
processed_message_ids = set()

# Function to process group messages
def process_group_message(message, thread_id, user_id):
    try:
        # Fetch user details using user_id
        user = cl.user_info(user_id)
        username = user.username  # Get the username of the sender
        
        if "/percentages" in message.lower():
            # Generate the first random percentage
            percentage1 = random.randint(0, 100)
            # Calculate the second percentage as the remaining value
            percentage2 = 100 - percentage1
            response = f"Here are your random percentages, {username}:\n1. {percentage1}%\n2. {percentage2}%"
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
                print(f"Processing group chat with ID: {thread.id}")
                messages = cl.direct_messages(thread.id)
                for message in messages:
                    # Process only unread messages
                    if message.id not in processed_message_ids:
                        user_id = message.user_id  # Get the user_id of the sender
                        print(f"New message from user_id {user_id} in group (ID: {thread.id}): {message.text}")
                        process_group_message(message.text, thread.id, user_id)
                        # Mark this message as processed
                        processed_message_ids.add(message.id)

        time.sleep(10)
except KeyboardInterrupt:
    print("Bot stopped.")
except Exception as e:
    print(f"Error: {e}")
