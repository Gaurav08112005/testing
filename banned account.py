import os.path
import csv
from pyrogram import Client

# Read API credentials from config file
with open('config.ini') as f:
    config = f.read().splitlines()

api_id = int(config[0].split('=')[1].strip())
api_hash = config[1].split('=')[1].strip()

# Create a session folder if it doesn't already exist
if not os.path.exists('sessions'):
    os.makedirs('sessions')

# Load phone numbers from csv file
with open('phone.csv') as f:
    phones = f.read().splitlines()

# Create a list to store banned accounts
banned_accounts = []

# Check each phone number for banned accounts
for phone_number in phones:
    # Log in and save the session file
    session_name = f'sessions/{phone_number}'
    with Client(session_name, api_id, api_hash) as client:
        client.start()
        print(f"Session file saved for {phone_number} in {session_name}")

        try:
            # Check if the account is banned
            client.send_message("spambot", "/start")
            client.send_message("spambot", "/stats")
            response = client.recv_message("spambot", timeout=10)
            if "This account is currently banned" in response.text:
                print(f"{phone_number} is banned")
                banned_accounts.append(phone_number)
            else:
                print(f"{phone_number} is not banned")
        except Exception as e:
            print(f"Error checking {phone_number}: {str(e)}")

        client.stop()

# Ask the user if they want to delete banned accounts
if banned_accounts:
    print("The following accounts are banned:")
    for phone_number in banned_accounts:
        print(phone_number)

    while True:
        delete = input("Do you want to delete all banned accounts? (y/n): ").lower()
        if delete == "y":
            # Remove banned accounts from phone.csv and session files
            with open('phone.csv', 'r') as f:
                reader = csv.reader(f)
                phone_numbers = list(reader)
            with open('phone.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                for row in phone_numbers:
                    if row[0] not in banned_accounts:
                        writer.writerow(row)
            for phone_number in banned_accounts:
                session_name = f'sessions/{phone_number}'
                if os.path.exists(session_name):
                    os.remove(session_name)
            print("Banned accounts deleted from phone.csv and session files.")
            break
        elif delete == "n":
            break
        else:
            print("Invalid input. Please enter y or n.")
else:
    print("No banned accounts found in phone.csv.")
