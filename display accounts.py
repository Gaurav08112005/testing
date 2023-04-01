import os.path
from pyrogram import Client

# Read API credentials from config file
with open('config.ini') as f:
    config = f.read().splitlines()

api_id = int(config[0].split('=')[1].strip())
api_hash = config[1].split('=')[1].strip()

# Load phone numbers from csv file
with open('phone.csv') as f:
    phones = f.read().splitlines()

for phone_number in phones:
    # Check if session file exists
    session_name = f'sessions/{phone_number}'
    if os.path.isfile(session_name):
        # Try to log in and check if session is authorized
        with Client(session_name, api_id, api_hash) as client:
            try:
                client.start(phone_number=phone_number)
                is_authorized = client.is_user_authorized()
                client.stop()
            except Exception as e:
                is_authorized = False
            
            if is_authorized:
                print(f"{phone_number}: Session file exists and is fully authorized.")
            else:
                print(f"{phone_number}: Session file exists but is not fully authorized.")
    else:
        print(f"{phone_number}: Session file does not exist.")

