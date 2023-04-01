import csv
import os.path
from pyrogram import Client

# Read API credentials from config file
with open('config.ini') as f:
    config = f.read().splitlines()

api_id = int(config[0].split('=')[1].strip())
api_hash = config[1].split('=')[1].strip()
phone_number = config[2].split('=')[1].strip()

# Create a session folder if it doesn't already exist
if not os.path.exists('sessions'):
    os.makedirs('sessions')

# Log in and save the session file
session_name = f'sessions/{phone_number}'

if os.path.exists(session_name):
    with Client(session_name, api_id, api_hash) as client:
        client.start()
        print(f"Session file loaded for {phone_number}")
else:
    with Client(session_name, api_id, api_hash) as client:
        client.start()
        print(f"New session created for {phone_number}")
