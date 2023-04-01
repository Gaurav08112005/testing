from pyrogram import Client, filters
import time

# Read API credentials from config file
with open('config.ini') as f:
    config = f.read().splitlines()

api_id = int(config[0].split('=')[1].strip())
api_hash = config[1].split('=')[1].strip()

# Load phone numbers from csv file
with open('phone.csv') as f:
    phones = f.read().splitlines()

# Define the spam bot username
spam_bot_username = 'spam_bot'

# Function to check if a user is limited
def check_if_limited(client, username):
    try:
        # Send a message to the spam bot and check if it's delivered
        message = client.send_message(spam_bot_username, f"/start {username}")
        time.sleep(5)
        message.delete()
        return False
    except Exception as e:
        # If the message is not delivered, check if it's due to user being limited
        if "user is limited" in str(e):
            return True
        else:
            return False

# Loop through the authorized accounts
for phone_number in phones:
    # Log in and save the session file
    session_name = f'sessions/{phone_number}'
    with Client(session_name, api_id, api_hash) as client:
        client.start()
        print(f"Session file saved for {phone_number} in {session_name}")

        # Load user IDs from members folder
        with open(f'members/{phone_number}.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                user_id = int(row[0])
                username = row[1]

                # Check if the user is limited
                is_limited = check_if_limited(client, username)
                if is_limited:
                    print(f"{username} is limited")
                else:
                    print(f"{username} is not limited")

                time.sleep(5)  # wait for 5 seconds before checking the next user
