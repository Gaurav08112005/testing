import os
import pyrogram
from pyrogram import Client
from faker import Faker

# Read API credentials from config file
with open('config.ini') as f:
    config = f.read().splitlines()

api_id = config[0]
api_hash = config[1]
phone_number = input("Enter your phone number (with country code): ")

# Create a session folder if it doesn't already exist
if not os.path.exists('sessions'):
    os.makedirs('sessions')

# Start the client session
session_name = f'sessions/{phone_number}'
client = Client(session_name, api_id, api_hash)
client.start(phone_number)

# Get verification code
code = input("Enter the code you received: ")

# Generate random first and last name using the faker library
fake = Faker()
first_name = fake.first_name()
last_name = fake.last_name()

# Register the new account
try:
    client.sign_up(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        phone_code=code
    )
    print("Account created successfully!")
except Exception as e:
    print(f"Error creating account: {e}")
